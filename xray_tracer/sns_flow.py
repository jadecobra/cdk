import aws_cdk
import constructs
import well_architected_constructs.lambda_function


class SnsFlow(aws_cdk.Stack):
    def __init__(self, scope: constructs.Construct, id: str, sns_topic: aws_cdk.aws_sns.ITopic = None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        topic = aws_cdk.aws_sns.Topic(self, 'TheXRayTracerSnsTopic', display_name='The XRay Tracer CDK Pattern Topic')

        sns_publisher = well_architected_constructs.lambda_function.create_python_lambda_function(
            self, function_name="sns_publish",
            environment_variables={
                "TOPIC_ARN": topic.topic_arn
            }
        )
        sns_subscriber = well_architected_constructs.lambda_function.create_python_lambda_function(self, "sns_subscribe")

        topic.grant_publish(sns_publisher)
        topic.add_subscription(
            aws_cdk.aws_sns_subscriptions.LambdaSubscription(
                sns_subscriber
            )
        )

        apigw_topic = aws_cdk.aws_sns.Topic.from_topic_arn(self, 'SNSTopic', sns_topic.topic_arn)
        apigw_topic.add_subscription(aws_cdk.aws_sns_subscriptions.LambdaSubscription(sns_publisher))

    def create_sns_publisher(self, topic: aws_cdk.aws_sns.ITopic):
        return well_architected_constructs.lambda_function.create_python_lambda_function(
            self, function_name="sns_publish",
            environment_variables={
                "TOPIC_ARN": topic.topic_arn
            }
        )