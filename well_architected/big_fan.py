from aws_cdk import (
    aws_lambda,
    aws_lambda_event_sources,
    aws_apigateway as api_gw,
    aws_iam as iam,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_sqs as sqs,
    core as cdk
)
import json


class BigFan(cdk.Stack):

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

        ###
        # API Gateway Creation
        # This is complicated because it transforms the incoming json payload into a query string url
        # this url is used to post the payload to sns without a lambda inbetween
        ###

        gateway = api_gw.RestApi(
            self, 'theBigFanAPI',
            deploy_options=api_gw.StageOptions(
                metrics_enabled=True,
                logging_level=api_gw.MethodLoggingLevel.INFO,
                data_trace_enabled=True,
                stage_name='prod'
            )
        )

        # Give our gateway permissions to interact with SNS
        api_gw_sns_role = iam.Role(self, 'DefaultLambdaHanderRole',
                                   assumed_by=iam.ServicePrincipal('apigateway.amazonaws.com'))
        topic.grant_publish(api_gw_sns_role)

        # shortening the lines of later code
        schema = api_gw.JsonSchema
        schema_type = api_gw.JsonSchemaType

        # Because this isn't a proxy integration, we need to define our response model
        response_model = gateway.add_model('ResponseModel',
                                           content_type='application/json',
                                           model_name='ResponseModel',
                                           schema=schema(schema=api_gw.JsonSchemaVersion.DRAFT4,
                                                         title='pollResponse',
                                                         type=schema_type.OBJECT,
                                                         properties={
                                                             'message': schema(type=schema_type.STRING)
                                                         }))

        error_response_model = gateway.add_model('ErrorResponseModel',
                                                 content_type='application/json',
                                                 model_name='ErrorResponseModel',
                                                 schema=schema(schema=api_gw.JsonSchemaVersion.DRAFT4,
                                                               title='errorResponse',
                                                               type=schema_type.OBJECT,
                                                               properties={
                                                                   'state': schema(type=schema_type.STRING),
                                                                   'message': schema(type=schema_type.STRING)
                                                               }))

        request_template = "Action=Publish&" + \
                           "TargetArn=$util.urlEncode('" + topic.topic_arn + "')&" + \
                           "Message=$util.urlEncode($input.path('$.message'))&" + \
                           "Version=2010-03-31&" + \
                           "MessageAttributes.entry.1.Name=status&" + \
                           "MessageAttributes.entry.1.Value.DataType=String&" + \
                           "MessageAttributes.entry.1.Value.StringValue=$util.urlEncode($input.path('$.status'))"

        # This is the VTL to transform the error response
        error_template = {
            "state": 'error',
            "message": "$util.escapeJavaScript($input.path('$.errorMessage'))"
        }
        error_template_string = json.dumps(error_template, separators=(',', ':'))

        # This is how our gateway chooses what response to send based on selection_pattern
        integration_options = api_gw.IntegrationOptions(
            credentials_role=api_gw_sns_role,
            request_parameters={
                'integration.request.header.Content-Type': "'application/x-www-form-urlencoded'"
            },
            request_templates={
                "application/json": request_template
            },
            passthrough_behavior=api_gw.PassthroughBehavior.NEVER,
            integration_responses=[
                api_gw.IntegrationResponse(
                    status_code='200',
                    response_templates={
                        "application/json": json.dumps(
                            {"message": 'message added to topic'})
                    }),
                api_gw.IntegrationResponse(
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
            .add_method('POST', api_gw.Integration(type=api_gw.IntegrationType.AWS,
                                                   integration_http_method='POST',
                                                   uri='arn:aws:apigateway:us-east-1:sns:path//',
                                                   options=integration_options
                                                   ),
                        method_responses=[
                            api_gw.MethodResponse(status_code='200',
                                                  response_parameters={
                                                      'method.response.header.Content-Type': True,
                                                      'method.response.header.Access-Control-Allow-Origin': True,
                                                      'method.response.header.Access-Control-Allow-Credentials': True
                                                  },
                                                  response_models={
                                                      'application/json': response_model
                                                  }),
                            api_gw.MethodResponse(status_code='400',
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
