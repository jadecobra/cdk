from aws_cdk.core import Stack, Construct, Duration
from aws_cdk.aws_lambda import Function, Code, Runtime


class LambdaFunction(Stack):

    def __init__(self, scope: Construct, id: str, function_name=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.lambda_function = Function(
            self, "LambdaFunction",
            runtime=Runtime.PYTHON_3_8,
            handler=f'{function_name}.handler',
            code=Code.from_asset("lambda_functions"),
            timeout=Duration.seconds(60)
        )