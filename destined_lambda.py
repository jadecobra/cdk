import aws_cdk
import constructs
import json
import well_architected
import well_architected_lambda


class DestinedLambda(well_architected.WellArchitectedStack):

    def create_lambda_function(
        self, on_failure=None, on_success=None,
        function_name=None, duration=3, retry_attempts=2
    ):
        return well_architected_lambda.LambdaFunctionConstruct(
            self, function_name,
            retry_attempts=retry_attempts,
            on_success=on_success,
            on_failure=on_failure,
            duration=duration
        ).lambda_function

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        event_bus = aws_cdk.aws_events.EventBus(
            self, 'EventBus',
            event_bus_name='the-destined-lambda',
        )
        sns_topic = aws_cdk.aws_sns.Topic(
            self, 'SNSTopic',
            display_name='The Destined Lambda CDK Pattern Topic'
        )

        sns_topic.add_subscription(
            aws_cdk.aws_sns_subscriptions.LambdaSubscription(
                self.create_lambda_function(
                    function_name="destined_lambda",
                    retry_attempts=0,
                    on_success=aws_cdk.aws_lambda_destinations.EventBridgeDestination(event_bus=event_bus),
                    on_failure=aws_cdk.aws_lambda_destinations.EventBridgeDestination(event_bus=event_bus),
                    duration=None,
                )
            )
        )

        ###
        # EventBridge Rule to send events to our success lambda
        # Notice how we can still do event filtering based on the json payload returned by the destined lambda
        ###
        success_rule = aws_cdk.aws_events.Rule(
            self, 'successRule',
            event_bus=event_bus,
            description='all success events are caught here and logged centrally',
            event_pattern=aws_cdk.aws_events.EventPattern(
                detail={
                    "requestContext": {
                        "condition": ["Success"]
                    },
                    "responsePayload": {
                        "source": ["cdkpatterns.the-destined-lambda"],
                        "action": ["message"]
                    }
                }
            )
        )
        success_rule.add_target(
            aws_cdk.aws_events_targets.LambdaFunction(
                self.create_lambda_function(
                    function_name="success_lambda",
                )
            )
        )

        ###
        # This is a lambda that will be called by onFailure for destinedLambda
        # It simply prints the event it receives to the cloudwatch logs.
        # Notice how it includes the message that came into destined lambda to make it fail so you have
        # everything you need to do retries or manually investigate
        ###

        ###
        # EventBridge Rule to send events to our failure lambda
        ###
        failure_rule = aws_cdk.aws_events.Rule(
            self, 'failureRule',
            event_bus=event_bus,
            description='all failure events are caught here and logged centrally',
            event_pattern=aws_cdk.aws_events.EventPattern(
                detail={
                    "responsePayload": {
                        "errorType": ["Error"]
                    }
                }
            )
        )
        failure_rule.add_target(
            aws_cdk.aws_events_targets.LambdaFunction(
                self.create_lambda_function(
                    function_name="failure_lambda",
                )
            )
        )

        ###
        # API Gateway Creation
        # This is complicated because it transforms the incoming json payload into a query string url
        # this url is used to post the payload to sns without a lambda inbetween
        ###

        gateway = aws_cdk.aws_apigateway.RestApi(
            self, 'RestApi',
            deploy_options=aws_cdk.aws_apigateway.StageOptions(
                metrics_enabled=True,
                logging_level=aws_cdk.aws_apigateway.MethodLoggingLevel.INFO,
                data_trace_enabled=True,
                stage_name='prod'
            )
        )
        # Give our gateway permissions to interact with SNS
        api_gw_sns_role = aws_cdk.aws_iam.Role(
            self, 'ApiGatewaySNSRole',
            assumed_by=aws_cdk.aws_iam.ServicePrincipal('apigateway.amazonaws.com')
        )
        sns_topic.grant_publish(api_gw_sns_role)

        # shortening the lines of later code
        schema = aws_cdk.aws_apigateway.JsonSchema
        schema_type = aws_cdk.aws_apigateway.JsonSchemaType

        # Because this isn't a proxy integration, we need to define our response model
        response_model = gateway.add_model(
            'ResponseModel',
            content_type='application/json',
            model_name='ResponseModel',
            schema=schema(schema=aws_cdk.aws_apigateway.JsonSchemaVersion.DRAFT4,
                            title='pollResponse',
                            type=schema_type.OBJECT,
                            properties={
                                'message': schema(type=schema_type.STRING)
                            }))

        error_response_model = gateway.add_model(
            'ErrorResponseModel',
            content_type='application/json',
            model_name='ErrorResponseModel',
            schema=schema(schema=aws_cdk.aws_apigateway.JsonSchemaVersion.DRAFT4,
                        title='errorResponse',
                        type=schema_type.OBJECT,
                        properties={
                            'state': schema(type=schema_type.STRING),
                            'message': schema(type=schema_type.STRING)
                        }))

        request_template = "Action=Publish&" + \
                           "TargetArn=$util.urlEncode('" + sns_topic.topic_arn + "')&" + \
                           "Message=please $input.params().querystring.get('mode')&" + \
                           "Version=2010-03-31"

        # This is the VTL to transform the error response
        error_template = {
            "state": 'error',
            "message": "$util.escapeJavaScript($input.path('$.errorMessage'))"
        }
        error_template_string = json.dumps(error_template, separators=(',', ':'))

        # This is how our gateway chooses what response to send based on selection_pattern
        integration_options = aws_cdk.aws_apigateway.IntegrationOptions(
            credentials_role=api_gw_sns_role,
            request_parameters={
                'integration.request.header.Content-Type': "'application/x-www-form-urlencoded'"
            },
            request_templates={
                "application/json": request_template
            },
            passthrough_behavior=aws_cdk.aws_apigateway.PassthroughBehavior.NEVER,
            integration_responses=[
                aws_cdk.aws_apigateway.IntegrationResponse(
                    status_code='200',
                    response_templates={
                        "application/json": json.dumps(
                            {"message": 'Message added to SNS topic'})
                    }),
                aws_cdk.aws_apigateway.IntegrationResponse(
                    selection_pattern="^\[Error\].*",
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

        # Add an SendEvent endpoint onto the gateway
        gateway.root.add_resource('SendEvent') \
            .add_method(
                'GET', aws_cdk.aws_apigateway.Integration(
                    type=aws_cdk.aws_apigateway.IntegrationType.AWS,
                    integration_http_method='POST',
                    uri='arn:aws:apigateway:us-east-1:sns:path//',
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
                        }),
                    aws_cdk.aws_apigateway.MethodResponse(
                        status_code='400',
                        response_parameters={
                            'method.response.header.Content-Type': True,
                            'method.response.header.Access-Control-Allow-Origin': True,
                            'method.response.header.Access-Control-Allow-Credentials': True
                        },
                        response_models={
                            'application/json': error_response_model
                        }),
                ]
        )
