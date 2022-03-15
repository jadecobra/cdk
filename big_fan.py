from pickle import STACK_GLOBAL
from aws_cdk import (
    aws_lambda,
    aws_lambda_event_sources,
    aws_apigateway as api_gateway,
    aws_iam as iam,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_sqs as sqs,
    core as cdk
)
import json


class BigFan(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        topic = sns.Topic(
            self, 'theBigFanTopic',
            display_name='The Big Fan CDK Pattern Topic'
        )
        logging_lambda_function = self.create_lambda_function("big_fan_logger")

        for queue_name, filter_name in (
            ('BigFanTopicStatusCreatedSubscriberQueue', 'allowlist'),
            ('BigFanTopicAnyOtherStatusSubscriberQueue', 'denylist'),
        ):
            sqs_queue = self.create_sqs_queue_with_subscription(
                queue_name=queue_name,
                sns_topic=topic,
                filter_name=filter_name
            )
            self.connect_lambda_function_with_sqs_queue(
                lambda_function=logging_lambda_function,
                sqs_queue=sqs_queue
            )

        api = api_gateway.RestApi(
            self, 'theBigFanAPI',
            deploy_options=self.deploy_options()
        )

        api_gateway_service_role_for_sns = iam.Role(
            self, 'DefaultLambdaHanderRole',
            assumed_by=iam.ServicePrincipal('apigateway.amazonaws.com')
        )

        topic.grant_publish(api_gateway_service_role_for_sns)

        self.add_resource_method(
            api=api,
            iam_role=api_gateway_service_role_for_sns,
            topic_arn=topic.topic_arn
        )

    @staticmethod
    def deploy_options():
        return api_gateway.StageOptions(
            metrics_enabled=True,
            logging_level=api_gateway.MethodLoggingLevel.INFO,
            data_trace_enabled=True,
            stage_name='prod'
        )

    def add_resource_method(self, api=None, iam_role=None, topic_arn=None):
        api.root.add_resource(
            'SendEvent'
        ).add_method(
            'POST',
            api_gateway.Integration(
                type=api_gateway.IntegrationType.AWS,
                integration_http_method='POST',
                uri='arn:aws:apigateway:us-east-1:sns:path//',
                options=self.integration_options(
                    iam_role=iam_role,
                    topic_arn=topic_arn,
                )
            ),
            method_responses=[
                self.create_method_response(
                    status_code=200,
                    response_model=self.create_api_response_model(
                        api=api,
                        model_name='ResponseModel',
                        title='pollResponse',
                        properties={
                            'message': self.json_schema_string()
                        }
                    )
                ),
                self.create_method_response(
                    status_code=400,
                    response_model=self.create_api_response_model(
                        api=api,
                        model_name='ErrorResponseModel',
                        title='errorResponse',
                        properties={
                            'state': self.json_schema_string(),
                            'message': self.json_schema_string()
                        }
                    )
                )
            ]
        )

    def integration_options(self, iam_role=None, topic_arn=None):
        return api_gateway.IntegrationOptions(
            credentials_role=iam_role,
            request_parameters={
                'integration.request.header.Content-Type': "'application/x-www-form-urlencoded'"
            },
            request_templates=self.create_json_template(
                (
                    "Action=Publish&"
                    f"TargetArn=$util.urlEncode('{topic_arn}')&"
                    "Message=$util.urlEncode($input.path('$.message'))&"
                    "Version=2010-03-31&"
                    "MessageAttributes.entry.1.Name=status&"
                    "MessageAttributes.entry.1.Value.DataType=String&"
                    "MessageAttributes.entry.1.Value.StringValue=$util.urlEncode($input.path('$.status'))"
                )
            ),
            passthrough_behavior=api_gateway.PassthroughBehavior.NEVER,
            integration_responses=[
                api_gateway.IntegrationResponse(
                    status_code='200',
                    response_templates=self.create_json_template(
                        json.dumps(
                            {"message": 'message added to topic'}
                        )
                    )
                ),
                api_gateway.IntegrationResponse(
                    selection_pattern="^\[Error\].*",
                    status_code='400',
                    response_templates=self.create_json_template(
                        json.dumps(
                            {
                                "state": 'error',
                                "message": "$util.escapeJavaScript($input.path('$.errorMessage'))"
                            },
                            separators=(',', ':')
                        )
                    ),
                    response_parameters={
                        'method.response.header.Content-Type': "'application/json'",
                        'method.response.header.Access-Control-Allow-Origin': "'*'",
                        'method.response.header.Access-Control-Allow-Credentials': "'true'"
                    }
                )
            ]
        )

    @staticmethod
    def json_schema_string():
        return api_gateway.JsonSchema(type=api_gateway.JsonSchemaType.STRING)

    @staticmethod
    def create_api_response_model(api=None, model_name=None, title=None, properties=None):
        return api.add_model(
            model_name,
            content_type='application/json',
            model_name=model_name,
            schema=api_gateway.JsonSchema(
                schema=api_gateway.JsonSchemaVersion.DRAFT4,
                title=title,
                type=api_gateway.JsonSchemaType.OBJECT,
                properties=properties
            )
        )

    @staticmethod
    def create_json_template(template):
        return {'application/json': template}

    def create_method_response(self, status_code=None, response_model=None):
        return api_gateway.MethodResponse(
            status_code=str(status_code),
            response_parameters={
                'method.response.header.Content-Type': True,
                'method.response.header.Access-Control-Allow-Origin': True,
                'method.response.header.Access-Control-Allow-Credentials': True
            },
            response_models=self.create_json_template(response_model)
        )

    def create_sqs_queue(self, queue_name):
        return sqs.Queue(
            self, queue_name,
            visibility_timeout=cdk.Duration.seconds(300),
            queue_name=queue_name
        )

    def create_sqs_queue_with_subscription(self, queue_name=None, sns_topic=None, filter_name=None):
        sqs_queue = self.create_sqs_queue(queue_name)
        sns_topic.add_subscription(
            subscriptions.SqsSubscription(
                sqs_queue,
                raw_message_delivery=True,
                filter_policy={
                    'status': sns.SubscriptionFilter.string_filter(
                        **{filter_name: ['created']}
                    )
                }
            )
        )
        return sqs_queue

    @staticmethod
    def connect_lambda_function_with_sqs_queue(lambda_function=None, sqs_queue=None):
        if sqs_queue is not None or lambda_function is not None:
            sqs_queue.grant_consume_messages(lambda_function)
            lambda_function.add_event_source(aws_lambda_event_sources.SqsEventSource(sqs_queue))

    def create_lambda_function(self, function_name):
        return aws_lambda.Function(
            self, function_name,
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            handler=f"{function_name}.handler",
            code=aws_lambda.Code.from_asset(f"lambda_functions/{function_name}")
        )