import aws_cdk.core
import aws_cdk.aws_lambda
import aws_cdk.aws_lambda_event_sources
import aws_cdk.aws_dynamodb
import aws_cdk.aws_apigateway
import aws_cdk.aws_iam
import json

class DynamoStreamer(aws_cdk.core.Stack):

    def __init__(self, scope: aws_cdk.core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        rest_api = self.create_rest_api()
        api_gateway_service_role = self.create_api_gateway_service_role()
        partition_key = 'message'
        dynamodb_table = self.create_dynamodb_table(partition_key)
        dynamodb_table.grant_read_write_data(api_gateway_service_role)
        self.create_lambda_function_with_dynamodb_event_source(dynamodb_table)

        (
            rest_api.root
                    .add_resource('InsertItem')
                    .add_method(
                        'POST',
                        self.integrate_rest_api_with_dynamodb_put_item(
                            api_gateway_service_role=api_gateway_service_role,
                            dynamodb_table_name=dynamodb_table.table_name
                        ),
                        method_responses=self.create_method_responses(
                            rest_api=rest_api,
                            dynamodb_partition_key=partition_key
                        )
                    )
        )


    def create_api_integration_options(self, api_gateway_service_role=None, dynamodb_table_name=None):
        return aws_cdk.aws_apigateway.IntegrationOptions(
            credentials_role=api_gateway_service_role,
            request_templates=self.request_template(dynamodb_table_name),
            passthrough_behavior=aws_cdk.aws_apigateway.PassthroughBehavior.NEVER,
            integration_responses=self.get_integration_responses()
        )

    def integrate_rest_api_with_dynamodb_put_item(self, api_gateway_service_role=None, dynamodb_table_name=None):
        return aws_cdk.aws_apigateway.Integration(
            type=aws_cdk.aws_apigateway.IntegrationType.AWS,
            integration_http_method='POST',
            uri='arn:aws:apigateway:us-east-1:dynamodb:action/PutItem',
            options=self.create_api_integration_options(
                api_gateway_service_role=api_gateway_service_role,
                dynamodb_table_name=dynamodb_table_name
            )
        )

    @staticmethod
    def create_response_parameters(content_type=True, origin=True, credentials=True):
        return {
            'method.response.header.Content-Type': content_type,
            'method.response.header.Access-Control-Allow-Origin': origin,
            'method.response.header.Access-Control-Allow-Credentials': credentials,
        }

    def create_method_responses(self, rest_api=None, dynamodb_partition_key='message'):
        return [
            aws_cdk.aws_apigateway.MethodResponse(
                status_code=status_code,
                response_parameters=self.create_response_parameters(),
                response_models={ 'application/json': response_model },
            ) for status_code, response_model in self.create_response_models(
                rest_api=rest_api, dynamodb_partition_key=dynamodb_partition_key
            )
        ]

    def create_dynamodb_table(self, partition_key):
        return aws_cdk.aws_dynamodb.Table(
            self, "DynamoDbTable",
            stream=aws_cdk.aws_dynamodb.StreamViewType.NEW_IMAGE,
            partition_key=aws_cdk.aws_dynamodb.Attribute(
                name=partition_key,
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
            self, 'ApiGatewayServiceRole',
            assumed_by=aws_cdk.aws_iam.ServicePrincipal('apigateway.amazonaws.com')
        )

    @staticmethod
    def json_string():
        return aws_cdk.aws_apigateway.JsonSchema(type=aws_cdk.aws_apigateway.JsonSchemaType.STRING)

    def create_json_schema(self, partition_key=None, response_type='pollResponse', additional_properties=None):
        properties = [partition_key]
        properties.append(additional_properties) if additional_properties else None
        return aws_cdk.aws_apigateway.JsonSchema(
            schema=aws_cdk.aws_apigateway.JsonSchemaVersion.DRAFT4,
            title=response_type,
            type=aws_cdk.aws_apigateway.JsonSchemaType.OBJECT,
            properties={ key: self.json_string() for key in properties }
        )

    def create_response_models(self, rest_api=None, dynamodb_partition_key=None):
        return (
            (
                '200',
                self.add_response_model_to_rest_api(
                    rest_api=rest_api,
                    schema=self.create_json_schema(dynamodb_partition_key)
                )
            ),
            (
                '400',
                self.add_response_model_to_rest_api(
                    rest_api=rest_api,
                    model_name='ErrorResponseModel',
                    schema=self.create_json_schema(
                        dynamodb_partition_key,
                        response_type='errorResponse',
                        additional_properties='state',
                    )
                )
            )
        )

    def add_response_model_to_rest_api(self, rest_api=None, model_name='ResponseModel', schema=None):
        return rest_api.add_model(
            model_name,
            content_type='application/json',
            model_name=model_name,
            schema=schema
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

    def get_integration_responses(self):
        return [
            aws_cdk.aws_apigateway.IntegrationResponse(
                status_code='200',
                response_templates=self.application_json_template(
                    template={"message": 'item added to db'},
                    separators=None
                )
            ),
            aws_cdk.aws_apigateway.IntegrationResponse(
                selection_pattern="^\[BadRequest\].*",
                status_code='400',
                response_templates=self.error_response_template(),
                response_parameters=self.create_response_parameters(
                    content_type="'application/json'",
                    origin="'*'",
                    credentials="'true'",
                )
            )
        ]