import aws_cdk
import constructs

from aws_cdk.aws_lambda import Function
from aws_cdk.aws_apigatewayv2_alpha import HttpApi
from aws_cdk.aws_apigatewayv2_integrations_alpha import HttpLambdaIntegration
from api_gateway_cloudwatch import ApiGatewayCloudWatch
from well_architected import WellArchitectedFrameworkConstruct


class LambdaHttpApiGateway(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, id: str, lambda_function: Function, error_topic=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.http_api = HttpApi(
            self, 'HttpAPI',
            default_integration=HttpLambdaIntegration(
                'HTTPLambdaIntegration',
                handler=lambda_function
            )
        )

        ApiGatewayCloudWatch(
            self, 'ApiGatewayCloudWatch',
            api_id=self.http_api.http_api_id,
            error_topic=error_topic,
        )

        aws_cdk.CfnOutput(self, 'HTTP API Url', value=self.http_api.url)


class HttpApi(WellArchitectedFrameworkConstruct):

    def __init__(
        self, scope: constructs.Construct, id: str,
        error_topic=None, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.http_api = HttpApi(self, 'HttpAPI')

        ApiGatewayCloudWatch(
            self, 'ApiGatewayCloudWatch',
            api_id=self.http_api.http_api_id,
            error_topic=error_topic,
        )

        aws_cdk.CfnOutput(self, 'HTTP API Url', value=self.http_api.url)