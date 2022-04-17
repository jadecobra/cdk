import aws_cdk
import constructs

from aws_cdk import (
    aws_lambda as aws_lambda,
    aws_apigateway as api_gateway,
)


class TheSinglePurposeFunctionStack(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        adder = self.create_lambda_function('add')
        subtracter = self.create_lambda_function('subtract')
        multiplier = self.create_lambda_function('multiply')

        rest_api = api_gateway.LambdaRestApi(
            self, 'RestAPI',
            handler=adder,
            proxy=False
        )

        for path, lambda_function in {
            'add': adder,
            'subtract': subtracter,
            'multiply': multiplier,
        }.items():
            rest_api.root.resource_for_path(path).add_method(
                'GET', api_gateway.LambdaIntegration(lambda_function)
            )

    def create_lambda_function(self, function_name):
        return aws_lambda.Function(
            self, function_name,
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            handler=f"{function_name}.handler",
            code=aws_lambda.Code.from_asset("lambda_functions/single_purpose_lambda")
        )