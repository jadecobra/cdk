import aws_cdk
import constructs
import lambda_function


class SqsFlow(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, id: str, sns_topic: aws_cdk.aws_sns.ITopic = None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.sns_topic = sns_topic
        self.sqs_queue = aws_cdk.aws_sqs.Queue(
            self, 'RDSPublishQueue',
            visibility_timeout=aws_cdk.Duration.seconds(300)
        )
        self.sqs_publisher = self.create_sqs_publisher(
            sqs_queue=self.sqs_queue,
            sns_topic=self.sns_topic
        )
        self.sqs_subscriber = self.create_sqs_subscriber(self.sqs_queue)

    def create_sqs_publisher(self, sqs_queue: aws_cdk.aws_sqs.Queue=None, sns_topic: aws_cdk.aws_sns.ITopic=None):
        sqs_publisher = lambda_function.create_python_lambda_function(
            self, function_name="sqs",
            environment_variables={ "SQS_URL": sqs_queue.queue_url }
        )
        sns_topic.add_subscription(
            aws_cdk.aws_sns_subscriptions.LambdaSubscription(sqs_publisher)
        )
        sqs_queue.grant_send_messages(sqs_publisher)
        return sqs_publisher

    def create_sqs_subscriber(self, sqs_queue: aws_cdk.aws_sqs.Queue=None):
        sqs_subscriber = lambda_function.create_python_lambda_function(
            self, function_name="sqs_subscribe"
        )
        sqs_subscriber.add_event_source(aws_cdk.aws_lambda_event_sources.SqsEventSource(sqs_queue))
        sqs_queue.grant_consume_messages(sqs_subscriber)
        return sqs_subscriber