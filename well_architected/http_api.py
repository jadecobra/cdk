from aws_cdk.core import Stack, Construct, CfnOutput
from aws_cdk.aws_lambda import Function
from aws_cdk.aws_apigatewayv2 import HttpApi
from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration


class LambdaHTTPAPIGateway(Stack):

    def __init__(self, scope: Construct, id: str, lambda_function: Function, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.api_gateway = HttpApi(
            self, 'HttpAPI',
            default_integration=HttpLambdaIntegration(
                'HTTPLambdaIntegration',
                handler=lambda_function
            )
        )
        CfnOutput(self, 'HTTP API Url', value=self.api_gateway.url)