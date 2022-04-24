import aws_cdk
import constructs
import api_gateway_cloudwatch
import aws_cdk.aws_apigatewayv2_alpha
import aws_cdk.aws_apigatewayv2_integrations_alpha

from aws_cdk.aws_lambda import Function



class LambdaHttpApiGateway(aws_cdk.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        lambda_function: aws_cdk.aws_lambda.Function,
        error_topic=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.http_api = self.create_http_api_lambda_integration(lambda_function)
        api_gateway_cloudwatch.ApiGatewayCloudWatch(
            self, 'HttpApiGatewayCloudWatch',
            api_id=self.http_api.http_api_id,
            error_topic=error_topic,
        )

        aws_cdk.CfnOutput(self, 'HTTP API Url', value=self.http_api.url)

    def create_http_api_lambda_integration(self, lambda_function):
        return aws_cdk.aws_apigatewayv2_alpha.HttpApi(
            self, 'HttpApi',
            default_integration=aws_cdk.aws_apigatewayv2_integrations_alpha.HttpLambdaIntegration(
                'HTTPLambdaIntegration',
                handler=lambda_function
            )
        )


class HttpApi(well_architected.WellArchitectedFrameworkConstruct):

    def __init__(
        self, scope: constructs.Construct, id: str,
        error_topic=None, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.http_api = aws_cdk.aws_apigatewayv2_alpha.HttpApi(
            self, 'HttpAPI',
            create_default_stage=True,
        )

        api_gateway_cloudwatch.ApiGatewayCloudWatch(
            self, 'ApiGatewayCloudWatch',
            api_id=self.http_api.http_api_id,
            error_topic=error_topic,
        )

        aws_cdk.CfnOutput(self, 'HTTP API Url', value=self.http_api.url)