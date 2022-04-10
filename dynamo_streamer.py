import aws_cdk.core
import aws_cdk.aws_lambda
import aws_cdk.aws_lambda_event_sources
import aws_cdk.aws_dynamodb
import aws_cdk.aws_apigateway
import aws_cdk.aws_iam
import json

class DynamoStreamer(aws_cdk.core.Stack):

    @staticmethod
    def add_response_model_to_rest_api(rest_api):
        return rest_api.add_model(
            'ResponseModel',
            content_type='application/json',
            model_name='ResponseModel',
            schema=aws_cdk.aws_apigateway.JsonSchema(
                schema=aws_cdk.aws_apigateway.JsonSchemaVersion.DRAFT4,
                title='pollResponse',
                type=aws_cdk.aws_apigateway.JsonSchemaType.OBJECT,
                properties={
                    'message': aws_cdk.aws_apigateway.JsonSchema(type=aws_cdk.aws_apigateway.JsonSchemaType.STRING)
                }
            )
        )

    @staticmethod
    def add_error_response_model_to_rest_api(rest_api):
        return rest_api.add_model(
            'ErrorResponseModel',
            content_type='application/json',
            model_name='ErrorResponseModel',
            schema=aws_cdk.aws_apigateway.JsonSchema(
                schema=aws_cdk.aws_apigateway.JsonSchemaVersion.DRAFT4,
                title='errorResponse',
                type=aws_cdk.aws_apigateway.JsonSchemaType.OBJECT,
                properties={
                    'state': aws_cdk.aws_apigateway.JsonSchema(type=aws_cdk.aws_apigateway.JsonSchemaType.STRING),
                    'message': aws_cdk.aws_apigateway.JsonSchema(type=aws_cdk.aws_apigateway.JsonSchemaType.STRING)
                }
            )
        )

    @staticmethod
    def application_json_template(template, separators=(',', ':')):
        return {'application/json': json.dumps(template, separators=separators)}

    def request_template(self, table_name):
        return self.application_json_template({
            "TableName": table_name,
            "Item": {
                "message": {"S": "$input.path('$.message')"}
            }
        })

    def error_response_template(self):
        return self.application_json_template({
            "state": 'error',
            "message": "$util.escapeJavaScript($input.path('$.errorMessage'))"
        })

    def __init__(self, scope: aws_cdk.core.Construct, id: str, **kwargs) -> None:

        super().__init__(scope, id, **kwargs)

        api_gateway_service_role = self.create_api_gateway_service_role()
        rest_api = self.create_rest_api()
        dynamodb_table = self.create_dynamodb_table()
        self.create_lambda_function_with_dynamodb_event_source(dynamodb_table)
        dynamodb_table.grant_read_write_data(api_gateway_service_role)

        # Because this isn't a proxy integration, we need to define our response model
        response_model = self.add_response_model_to_rest_api(rest_api)
        error_response_model = self.add_error_response_model_to_rest_api(rest_api)

        # This is how our gateway chooses what response to send based on selection_pattern
        integration_options = aws_cdk.aws_apigateway.IntegrationOptions(
            credentials_role=api_gateway_service_role,
            request_templates=self.request_template(dynamodb_table.table_name),
            passthrough_behavior=aws_cdk.aws_apigateway.PassthroughBehavior.NEVER,
            integration_responses=[
                aws_cdk.aws_apigateway.IntegrationResponse(
                    status_code='200',
                    # response_templates={
                    #     "application/json": json.dumps(
                    #         {"message": 'item added to db'})
                    # }
                    response_templates=self.application_json_template(
                        {"message": 'item added to db'},
                        separators=None
                    )
                ),
                aws_cdk.aws_apigateway.IntegrationResponse(
                    selection_pattern="^\[BadRequest\].*",
                    status_code='400',
                    response_templates=self.error_response_template(),
                    response_parameters={
                        'method.response.header.Content-Type': "'application/json'",
                        'method.response.header.Access-Control-Allow-Origin': "'*'",
                        'method.response.header.Access-Control-Allow-Credentials': "'true'"
                    }
                )
            ]
        )

        # Add an InsertItem endpoint onto the gateway
        (
            rest_api.root
            .add_resource('InsertItem')
            .add_method(
                'POST', aws_cdk.aws_apigateway.Integration(
                    type=aws_cdk.aws_apigateway.IntegrationType.AWS,
                    integration_http_method='POST',
                    uri='arn:aws:apigateway:us-east-1:dynamodb:action/PutItem',
                    options=integration_options
                ),
                method_responses=[
                    aws_cdk.aws_apigateway.MethodResponse(
                        status_code='200',
                        response_parameters={
                            'method.response.header.Content-Type': True,
                            'method.response.header.Access-Control-Allow-Origin': True,
                            'method.response.header.Access-Control-Allow-Credentials': True
                        },
                        response_models={
                            'application/json': response_model
                        }
                    ),
                    aws_cdk.aws_apigateway.MethodResponse(
                        status_code='400',
                        response_parameters={
                            'method.response.header.Content-Type': True,
                            'method.response.header.Access-Control-Allow-Origin': True,
                            'method.response.header.Access-Control-Allow-Credentials': True
                        },
                        response_models={
                            'application/json': error_response_model
                        }
                    ),
                ]
            )
        )

    def create_dynamodb_table(self):
        return aws_cdk.aws_dynamodb.Table(
            self, "DynamoDbTable",
            stream=aws_cdk.aws_dynamodb.StreamViewType.NEW_IMAGE,
            partition_key=aws_cdk.aws_dynamodb.Attribute(
                name="message",
                type=aws_cdk.aws_dynamodb.AttributeType.STRING
            ),
        )

    def create_lambda_function_with_dynamodb_event_source(self, dynamodb_table):
        return aws_cdk.aws_lambda.Function(
            self, 'LambdaFunction',
            runtime=aws_cdk.aws_lambda.Runtime.PYTHON_3_8,
            handler="lambda.handler",
            code=aws_cdk.aws_lambda.Code.from_asset("lambda_functions/subscribe")
        ).add_event_source(
            aws_cdk.aws_lambda_event_sources.DynamoEventSource(
                table=dynamodb_table,
                starting_position=aws_cdk.aws_lambda.StartingPosition.LATEST
            )
        )

    def create_rest_api(self):
        return aws_cdk.aws_apigateway.RestApi(
            self, 'ApiGateway',
            deploy_options=aws_cdk.aws_apigateway.StageOptions(
                metrics_enabled=True,
                logging_level=aws_cdk.aws_apigateway.MethodLoggingLevel.INFO,
                data_trace_enabled=True,
                stage_name='prod'
            )
        )

    def create_api_gateway_service_role(self):
        return aws_cdk.aws_iam.Role(
            self, 'ApiGatewayRole',
            assumed_by=aws_cdk.aws_iam.ServicePrincipal('apigateway.amazonaws.com')
        )