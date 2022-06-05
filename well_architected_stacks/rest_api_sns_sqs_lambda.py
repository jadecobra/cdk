import aws_cdk
import constructs
import well_architected
import well_architected_constructs.lambda_function
import well_architected_constructs.rest_api
import well_architected_constructs.rest_api_sns


class ApiSnsSqsLambda(well_architected.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        sns_topic = self.create_sns_topic('The Big Fan CDK Pattern Topic')
        logging_lambda_function = self.create_lambda_function(
            error_topic=self.error_topic,
            function_name="big_fan_logger",
        )

        for queue_name, filter_name in (
            ('BigFanTopicStatusCreatedSubscriberQueue', 'allowlist'),
            ('BigFanTopicAnyOtherStatusSubscriberQueue', 'denylist'),
        ):
            sqs_queue = self.create_sqs_queue_with_subscription(
                queue_name=queue_name,
                sns_topic=sns_topic,
                filter_name=filter_name,
            )
            self.connect_lambda_function_with_sqs_queue(
                lambda_function=logging_lambda_function,
                sqs_queue=sqs_queue,
            )

        well_architected_constructs.rest_api_sns.RestApiSnsConstruct(
            self, 'RestApiSns',
            error_topic=self.error_topic,
            method='POST',
            request_templates=self.get_request_template(sns_topic.topic_arn),
        )


    def get_request_template(self, sns_topic_arn):
        return (
            f"Action=Publish&TargetArn=$util.urlEncode('{sns_topic_arn}')&Message=$util.urlEncode($input.path('$.message'))&Version=2010-03-31&MessageAttributes.entry.1.Name=status&MessageAttributes.entry.1.Value.DataType=String&MessageAttributes.entry.1.Value.StringValue=$util.urlEncode($input.path('$.status'))"
        )

    def create_sqs_queue(self, queue_name):
        return aws_cdk.aws_sqs.Queue(
            self, queue_name,
            visibility_timeout=aws_cdk.Duration.seconds(300),
            queue_name=queue_name
        )

    def create_sqs_queue_with_subscription(self, queue_name=None, sns_topic=None, filter_name=None):
        sqs_queue = self.create_sqs_queue(queue_name)
        sns_topic.add_subscription(
            aws_cdk.aws_sns_subscriptions.SqsSubscription(
                sqs_queue,
                raw_message_delivery=True,
                filter_policy={
                    'status': aws_cdk.aws_sns.SubscriptionFilter.string_filter(
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
            lambda_function.add_event_source(
                aws_cdk.aws_lambda_event_sources.SqsEventSource(sqs_queue)
            )

    def create_lambda_function(self, function_name=None, error_topic=None):
        return well_architected_constructs.lambda_function.LambdaFunctionConstruct(
            self, function_name,
            error_topic=error_topic,
        ).lambda_function