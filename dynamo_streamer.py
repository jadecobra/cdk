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

        dynamodb_table = aws_cdk.aws_dynamodb.Table(
            self, "DynamoDbTable",
            stream=aws_cdk.aws_dynamodb.StreamViewType.NEW_IMAGE,
            partition_key=aws_cdk.aws_dynamodb.Attribute(
                name="message",
                type=aws_cdk.aws_dynamodb.AttributeType.STRING
            ),
        )

        subscriber_lambda_function = aws_cdk.aws_lambda.Function(
            self, 'LambdaFunction',
            runtime=aws_cdk.aws_lambda.Runtime.PYTHON_3_8,
            handler="lambda.handler",
            code=aws_cdk.aws_lambda.Code.from_asset("lambda_functions/subscribe")
        )

        subscriber_lambda_function.add_event_source(
            aws_cdk.aws_lambda_event_sources..DynamoEventSource(
                table=dynamodb_table,
                starting_position=aws_cdk.aws_lambda.StartingPosition.LATEST
            )
        )

        # API Gateway Creation
        api_gateway = aws_cdk.api_gateway.RestApi(
            self, 'ApiGateway',
            deploy_options=aws_cdk.api_gateway.StageOptions(
                metrics_enabled=True,
                logging_level=aws_cdk.api_gateway.MethodLoggingLevel.INFO,
                data_trace_enabled=True,
                stage_name='prod'
            )
        )

        # Give our gateway permissions to interact with dynamodb
        api_gw_dynamo_role = aws_cdk.aws_iam.Role(
            self, 'ApiGatewayRole',
            assumed_by=aws_cdk.aws_iam.ServicePrincipal('apigateway.amazonaws.com')
        )
        dynamodb_table.grant_read_write_data(api_gw_dynamo_role)

        # shortening the lines of later code
        schema = aws_cdk.api_gateway.JsonSchema
        schema_type = aws_cdk.api_gateway.JsonSchemaType

        # Because this isn't a proxy integration, we need to define our response model
        response_model = api_gateway.add_model(
            'ResponseModel',
            content_type='application/json',
            model_name='ResponseModel',
            schema=schema(
                schema=aws_cdk.api_gateway.JsonSchemaVersion.DRAFT4,
                title='pollResponse',
                type=schema_type.OBJECT,
                properties={
                    'message': schema(type=schema_type.STRING)
                }
            )
        )

        error_response_model = api_gateway.add_model(
            'ErrorResponseModel',
            content_type='application/json',
            model_name='ErrorResponseModel',
            schema=schema(
                schema=aws_cdk.api_gateway.JsonSchemaVersion.DRAFT4,
                title='errorResponse',
                type=schema_type.OBJECT,
                properties={
                    'state': schema(type=schema_type.STRING),
                    'message': schema(type=schema_type.STRING)
                }
            )
        )

        # This is the VTL to transform our incoming JSON to a Dynamo Insert Query
        request_template = {
            "TableName": dynamodb_table.table_name,
            "Item": {
                "message": {"S": "$input.path('$.message')"}
            }
        }
        request_template_string = json.dumps(request_template, separators=(',', ':'))

        # This is the VTL to transform the error response
        error_template = {
            "state": 'error',
            "message": "$util.escapeJavaScript($input.path('$.errorMessage'))"
        }
        error_template_string = json.dumps(error_template, separators=(',', ':'))

        # This is how our gateway chooses what response to send based on selection_pattern
        integration_options = aws_cdk.api_gateway.IntegrationOptions(
            credentials_role=api_gw_dynamo_role,
            request_templates={
                "application/json": request_template_string
            },
            passthrough_behavior=aws_cdk.api_gateway.PassthroughBehavior.NEVER,
            integration_responses=[
                aws_cdk.api_gateway.IntegrationResponse(
                    status_code='200',
                    response_templates={
                        "application/json": json.dumps(
                            {"message": 'item added to db'})
                    }),
                aws_cdk.api_gateway.IntegrationResponse(
                    selection_pattern="^\[BadRequest\].*",
                    status_code='400',
                    response_templates={
                        "application/json": error_template_string
                    },
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
            api_gateway.root
            .add_resource('InsertItem')
            .add_method(
                'POST', aws_cdk.api_gateway.Integration(
                    type=aws_cdk.api_gateway.IntegrationType.AWS,
                    integration_http_method='POST',
                    uri='arn:aws:apigateway:us-east-1:dynamodb:action/PutItem',
                    options=integration_options
                ),
                method_responses=[
                    aws_cdk.api_gateway.MethodResponse(
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
                    aws_cdk.api_gateway.MethodResponse(
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
