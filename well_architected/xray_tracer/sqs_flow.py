from aws_cdk import (
    aws_sns as sns
)
from aws_cdk.core import Stack, Construct, Duration
from aws_cdk.aws_sqs import Queue
from aws_cdk.aws_sns_subscriptions import LambdaSubscription
from aws_cdk.aws_lambda_event_sources import SqsEventSource
from aws_cdk.aws_lambda import Code, Function, Runtime, Tracing
from aws_cdk.aws_sns import Topic
from lambda_function import LambdaFunctionConstruct
class SqsFlow(Stack):

    def __init__(self, scope: Construct, id: str, sns_topic_arn: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.sqs_queue = Queue(self, 'RDSPublishQueue', visibility_timeout=Duration.seconds(300))

        self.sqs_publisher = self.create_lambda_function(
            function_name="sqs",
            environment_variables={
                "SQS_URL": self.sqs_queue.queue_url
            }
        )

        self.sqs_subscriber = self.create_lambda_function(
            function_name="sqs_subscribe",
        )

        self.sqs_subscriber.add_event_source(SqsEventSource(self.sqs_queue))
        self.topic = Topic.from_topic_arn(self, 'SNSTopic', sns_topic_arn)
        self.topic.add_subscription(LambdaSubscription(self.sqs_publisher))
        self.add_permissions()

    def create_lambda_function(self, id=None, function_name=None, environment_variables=None):
        return LambdaFunctionConstruct(
            self, function_name,
            function_name=function_name,
            environment_variables=environment_variables,
        ).lambda_function

    def add_permissions(self):
        self.sqs_queue.grant_send_messages(self.sqs_publisher)
        self.sqs_queue.grant_consume_messages(self.sqs_subscriber)