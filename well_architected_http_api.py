import aws_cdk
import constructs
import api_gateway_cloudwatch
import aws_cdk.aws_apigatewayv2_alpha
import aws_cdk.aws_apigatewayv2_integrations_alpha
import well_architected


class HttpApi(well_architected.WellArchitectedFrameworkConstruct):

    def __init__(
        self, scope: constructs.Construct, id: str,
        error_topic=None,
        create_default_stage=None,
        default_integration=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.http_api = aws_cdk.aws_apigatewayv2_alpha.HttpApi(
            self, 'HttpAPI',
            create_default_stage=create_default_stage,
            default_integration=default_integration,
        )

        api_gateway_cloudwatch.ApiGatewayCloudWatch(
            self, 'ApiGatewayCloudWatch',
            api_id=self.http_api.http_api_id,
            error_topic=error_topic,
        )

        aws_cdk.CfnOutput(self, 'HTTP API Url', value=self.http_api.url)


class LambdaHttpApiGateway(well_architected.WellArchitectedFrameworkStack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        lambda_function: aws_cdk.aws_lambda.Function,
        error_topic=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.http_api = HttpApi(
            self, 'HttpApi',
            default_integration=aws_cdk.aws_apigatewayv2_integrations_alpha.HttpLambdaIntegration(
                'HTTPLambdaIntegration',
                handler=lambda_function
            )
        ).http_api
