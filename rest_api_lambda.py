import aws_cdk
import constructs


class RestApiLambdaStack(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, id: str, lambda_function: aws_cdk.aws_lambda.Function, error_topic:aws_cdk.aws_sns.Topic=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.rest_api = LambdaRestAPIGatewayConstruct(
            self, id,
            lambda_function=lambda_function,
            error_topic=error_topic,
            **kwargs
        )