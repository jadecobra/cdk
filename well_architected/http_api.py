from aws_cdk.core import Stack, Construct
from aws_cdk.aws_lambda import Function

import aws_cdk.aws_apigatewayv2 as api_gw
import aws_cdk.aws_apigatewayv2_integrations as integrations


class LambdaHTTPAPIGateway(Stack):

    def __init__(self, scope: Construct, id: str, lambda_function: Function, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.api_gateway = api_gw.HttpApi(
            self, 'HttpAPI',
            default_integration=integrations.HttpLambdaIntegration(
                'HTTPLambdaIntegration',
                handler=lambda_function
            )
        );