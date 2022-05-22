import aws_cdk
import constructs
import json
import well_architected_rest_api
import well_architected_lambda


class ApiSnsLambdaEventBridgeLambda(well_architected_rest_api.WellArchitectedRestApiSns):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        event_bus = self.create_event_bus(id)
        self.create_success_lambda(
            error_topic=self.error_topic,
            event_bus=event_bus,
        )
        self.create_failure_lambda(
            error_topic=self.error_topic,
            event_bus=event_bus,
        )

        sns_topic = self.create_sns_triggered_lambda(
            name='destined',
            event_bus=event_bus
        )

        self.create_rest_api_method(
            method='GET',
            rest_api=self.create_rest_api(self.error_topic),
            integration=self.create_api_sns_integration(sns_topic),
        )

    def create_success_lambda(self, event_bus=None, error_topic=None):
        return self.create_event_driven_lambda_function(
            function_name="success",
            error_topic=error_topic,
            event_bus=event_bus,
            description='all success events are caught here and logged centrally',
            response_payload={
                "source": ["cdkpatterns.the-destined-lambda"],
                "action": ["message"]
            },
            additional_details={
                "requestContext": {
                    "condition": ["Success"]
                }
            },
        )

    def create_failure_lambda(self, event_bus=None, error_topic=None):
        return self.create_event_driven_lambda_function(
            function_name="failure",
            error_topic=error_topic,
            event_bus=event_bus,
            description='all failure events are caught here and logged centrally',
            response_payload={
                "errorType": ["Error"]
            },
        )

    def create_sns_triggered_lambda(self, name=None, event_bus=None):
        sns_topic = self.create_sns_topic(f'{name}SnsTopic')
        sns_topic.add_subscription(
            aws_cdk.aws_sns_subscriptions.LambdaSubscription(
                self.create_lambda_function(
                    function_name=f"{name}_lambda",
                    retry_attempts=0,
                    on_success=aws_cdk.aws_lambda_destinations.EventBridgeDestination(event_bus=event_bus),
                    on_failure=aws_cdk.aws_lambda_destinations.EventBridgeDestination(event_bus=event_bus),
                    duration=None,
                    error_topic=self.error_topic
                )
            )
        )
        return sns_topic

    def create_event_bus(self, name):
        return aws_cdk.aws_events.EventBus(
            self, 'EventBus',
            event_bus_name=name,
        )

    def get_integration_options(self, iam_role=None, sns_topic_arn=None):
        return aws_cdk.aws_apigateway.IntegrationOptions(
            credentials_role=iam_role,
            request_parameters={
                'integration.request.header.Content-Type': "'application/x-www-form-urlencoded'"
            },
            request_templates={
                "application/json": f"""Action=Publish&TargetArn=$util.urlEncode('{sns_topic_arn}')&Message=please $input.params().querystring.get('mode')&Version=2010-03-31"""
            },
            passthrough_behavior=aws_cdk.aws_apigateway.PassthroughBehavior.NEVER,
            integration_responses=[
                self.create_integration_response(
                    status_code='200',
                    response_templates={"message": 'Message added to SNS topic'}
                ),
                self.create_integration_response(
                    status_code='400',
                    response_templates={
                        "message": "$util.escapeJavaScript($input.path('$.errorMessage'))",
                        "state": 'error',
                    },
                    selection_pattern="^\[Error\].*",
                    separators=(',', ':'),
                    response_parameters=self.create_response_parameters(
                        content_type="'application/json'",
                        allow_origin="'*'",
                        allow_credentials="'true'",
                    )
                )
            ]
        )

    def create_event_driven_lambda_function(
        self, event_bus=None, description=None, function_name=None, error_topic=None,
        response_payload=None, additional_details={}
    ):
        details = {
            "responsePayload": response_payload
        }
        details.update(additional_details)
        event_bridge_rule = aws_cdk.aws_events.Rule(
            self, f'event_bridge_rule_{function_name}',
            event_bus=event_bus,
            description=description,
            event_pattern=aws_cdk.aws_events.EventPattern(
                detail=details,
            )
        )
        event_bridge_rule.add_target(
            aws_cdk.aws_events_targets.LambdaFunction(
                self.create_lambda_function(
                    function_name=function_name,
                    error_topic=error_topic,
                )
            )
        )
        return event_bridge_rule

    # def create_response_model(
    #     self, rest_api=None, model_name=None, properties=None
    # ):
    #     property_keys = ['message']
    #     property_keys.append(properties) if properties else None
    #     return rest_api.add_model(
    #         model_name,
    #         content_type='application/json',
    #         model_name=model_name,
    #         schema=self.create_schema(
    #             title=model_name,
    #             properties={key: self.string_schema_type() for key in property_keys},
    #         )
    #     )

    # @staticmethod
    # def string_schema_type():
    #     return aws_cdk.aws_apigateway.JsonSchema(
    #         type=aws_cdk.aws_apigateway.JsonSchemaType.STRING
    #     )

    # @staticmethod
    # def create_schema(title=None, properties=None):
    #     return aws_cdk.aws_apigateway.JsonSchema(
    #         schema=aws_cdk.aws_apigateway.JsonSchemaVersion.DRAFT4,
    #         title=title,
    #         type=aws_cdk.aws_apigateway.JsonSchemaType.OBJECT,
    #         properties=properties
    #     )

    @staticmethod
    def create_integration_response(
        status_code=None, response_templates=None, response_parameters=None,
        selection_pattern=None, separators=None
    ):
        return aws_cdk.aws_apigateway.IntegrationResponse(
            status_code=status_code,
            selection_pattern=selection_pattern,
            response_templates={"application/json": json.dumps(response_templates, separators=separators)},
            response_parameters=response_parameters,
        )



    def create_lambda_function(
        self, on_failure=None, on_success=None,
        function_name=None, duration=3, retry_attempts=2,
        error_topic=None,
    ):
        return well_architected_lambda.LambdaFunctionConstruct(
            self, function_name,
            retry_attempts=retry_attempts,
            error_topic=error_topic,
            on_success=on_success,
            on_failure=on_failure,
            duration=duration
        ).lambda_function