from aws_cdk.core import Stack, Construct, CfnOutput
from aws_cdk.aws_lambda import Function
from aws_cdk.aws_apigatewayv2 import HttpApi
from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration
from api_gateway_cloudwatch import ApiGatewayCloudWatch, AltApiGatewayCloudWatch

class LambdaHttpApiGateway(Stack):

    def __init__(self, scope: Construct, id: str, lambda_function: Function, error_topic=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.http_api = HttpApi(
            self, 'HttpAPI',
            default_integration=HttpLambdaIntegration(
                'HTTPLambdaIntegration',
                handler=lambda_function
            )
        )
        self.api_gateway_cloudwatch = ApiGatewayCloudWatch(
            self, 'ApiGatewayCloudWatch',
            api_id=self.http_api.api_id,
            error_topic=error_topic,
        )
        self.api_gateway_cloudwatch_widgets = self.api_gateway_cloudwatch.api_gateway_cloudwatch_widgets
        CfnOutput(self, 'HTTP API Url', value=self.http_api.url)