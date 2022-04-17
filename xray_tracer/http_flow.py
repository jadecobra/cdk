from aws_cdk import Stack, Construct
from aws_cdk.aws_sns import ITopic
from aws_cdk.aws_sns_subscriptions import LambdaSubscription
from lambda_function import create_python_lambda_function


class HttpFlow(Stack):

    def __init__(self, scope: Construct, id: str, sns_topic: ITopic = None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        http_lambda = create_python_lambda_function(
            self, function_name="http",
        )
        sns_topic.add_subscription(LambdaSubscription(http_lambda))