import aws_cdk
import constructs
import well_architected
import well_architected_constructs.lambda_function


class HttpFlow(well_architected.Stack):

    def __init__(self, scope: constructs.Construct, id: str, sns_topic: aws_cdk.aws_sns.ITopic=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        http_lambda = well_architected_constructs.lambda_function.create_python_lambda_function(
            self, function_name="http",
        )
        sns_topic.add_subscription(
            aws_cdk.aws_sns_subscriptions.LambdaSubscription(http_lambda)
        )