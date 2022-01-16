from typing import ItemsView
from aws_cdk import (
    aws_lambda as _lambda,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    core
)
from aws_cdk.aws_sns import ITopic
from lambda_function import create_python_lambda_function



class SnsFlow(core.Stack):
    def __init__(self, scope: core.Construct, id: str, sns_topic: ITopic = None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        topic = sns.Topic(self, 'TheXRayTracerSnsTopic', display_name='The XRay Tracer CDK Pattern Topic')

        sns_publisher = self.create_sns_publisher(topic)
        sns_subscriber = create_python_lambda_function(self, "sns_subscribe")

        topic.grant_publish(sns_publisher)
        topic.add_subscription(subscriptions.LambdaSubscription(sns_subscriber))

        apigw_topic = sns.Topic.from_topic_arn(self, 'SNSTopic', sns_topic.topic_arn)
        apigw_topic.add_subscription(subscriptions.LambdaSubscription(sns_publisher))

    def create_sns_publisher(self, topic: ITopic):
        return create_python_lambda_function(
            self, function_name="sns_publish",
            environment_variables={
                "TOPIC_ARN": topic.topic_arn
            }
        )