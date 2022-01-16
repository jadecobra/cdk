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

        # SNS Topic creation
        topic = sns.Topic(self, 'TheXRayTracerSnsTopic', display_name='The XRay Tracer CDK Pattern Topic')

        sns_lambda = create_python_lambda_function(
            self, function_name="sns_publish",
            environment_variables={
                "TOPIC_ARN": topic.topic_arn
            }
        )
        topic.grant_publish(sns_lambda)
        apigw_topic = sns.Topic.from_topic_arn(self, 'SNSTopic', sns_topic.topic_arn)
        apigw_topic.add_subscription(subscriptions.LambdaSubscription(sns_lambda))
        sns_subscriber_lambda = create_python_lambda_function(self, "sns_subscribe")
        topic.add_subscription(subscriptions.LambdaSubscription(sns_subscriber_lambda))
