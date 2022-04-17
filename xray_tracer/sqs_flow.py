from aws_cdk import Stack, Construct, Duration
from aws_cdk.aws_sqs import Queue
from aws_cdk.aws_sns_subscriptions import LambdaSubscription
from aws_cdk.aws_lambda_event_sources import SqsEventSource
from aws_cdk.aws_sns import ITopic
from lambda_function import create_python_lambda_function
class SqsFlow(Stack):

    def __init__(self, scope: Construct, id: str, sns_topic: ITopic = None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.sns_topic = sns_topic
        self.sqs_queue = Queue(self, 'RDSPublishQueue', visibility_timeout=Duration.seconds(300))
        self.sqs_publisher = self.create_sqs_publisher(sqs_queue=self.sqs_queue, sns_topic=self.sns_topic)
        self.sqs_subscriber = self.create_sqs_subscriber(self.sqs_queue)

    def create_sqs_publisher(self, sqs_queue: Queue=None, sns_topic: ITopic=None):
        sqs_publisher = create_python_lambda_function(
            self, function_name="sqs",
            environment_variables={"SQS_URL": sqs_queue.queue_url}
        )
        sns_topic.add_subscription(LambdaSubscription(sqs_publisher))
        sqs_queue.grant_send_messages(sqs_publisher)
        return sqs_publisher

    def create_sqs_subscriber(self, sqs_queue: Queue=None):
        sqs_subscriber = create_python_lambda_function(self, function_name="sqs_subscribe")
        sqs_subscriber.add_event_source(SqsEventSource(sqs_queue))
        sqs_queue.grant_consume_messages(sqs_subscriber)
        return sqs_subscriber