import aws_cdk
import constructs
import well_architected
import well_architected_constructs.lambda_function
import well_architected_constructs.sns_lambda


class SnsLambdaSns(well_architected.Stack):

    def __init__(
        self, scope: constructs.Construct,
        id: str, sns_topic=None, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        topic = aws_cdk.aws_sns.Topic(
            self, 'SnsLambda',
            display_name='SnsLambda'
        )

        sns_publisher = self.create_sns_publisher(topic.topic_arn)
        topic.grant_publish(sns_publisher)
        topic.add_subscription(
            aws_cdk.aws_sns_subscriptions.LambdaSubscription(
                well_architected_constructs.lambda_function.create_python_lambda_function(
                    self, "sns_subscriber"
                )
            )
        )

        sns_topic.add_subscription(
            aws_cdk.aws_sns_subscriptions.LambdaSubscription(
                sns_publisher
            )
        )

    def create_sns_publisher(self, sns_topic_arn=None):
        return well_architected_constructs.lambda_function.create_python_lambda_function(
            self, function_name="sns_publisher",
            environment_variables={
                "TOPIC_ARN": sns_topic_arn
            }
        )