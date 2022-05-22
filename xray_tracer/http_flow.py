import aws_cdk
import constructs
import well_architected.constructs.lambda as lambda


class HttpFlow(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, id: str, sns_topic: aws_cdk.aws_sns.ITopic=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        http_lambda = lambda.create_python_lambda_function(
            self, function_name="http",
        )
        sns_topic.add_subscription(
            aws_cdk.aws_sns_subscriptions.LambdaSubscription(http_lambda)
        )