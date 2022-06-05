import aws_cdk
import constructs
import aws_cdk.aws_apigatewayv2_alpha
import aws_cdk.aws_apigatewayv2_integrations_alpha

import well_architected
import well_architected_constructs.api
import well_architected_constructs.api_lambda
import well_architected_constructs.lambda_function


class LambdaSinglePurpose(well_architected.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        adder = self.create_lambda_function('add')
        subtracter = self.create_lambda_function('subtract')
        multiplier = self.create_lambda_function('multiply')

        rest_api = self.create_rest_api(
            error_topic=self.error_topic,
            lambda_function=adder,
        )

        http_api = self.create_http_api(self.error_topic)

        for path, lambda_function in {
            'add': adder,
            'subtract': subtracter,
            'multiply': multiplier,
        }.items():
            rest_api.root.resource_for_path(path).add_method(
                'GET', aws_cdk.aws_apigateway.LambdaIntegration(lambda_function)
            )
            http_api.add_routes(
                path=f'/{path}',
                methods=[aws_cdk.aws_apigatewayv2_alpha.HttpMethod.GET],
                integration=aws_cdk.aws_apigatewayv2_integrations_alpha.HttpLambdaIntegration(
                    f'HttpApi{path.title()}Integration',
                    handler=lambda_function
                ),
            )

    def create_rest_api(self, error_topic=None, lambda_function=None):
        return well_architected_constructs.api_lambda.create_rest_api_lambda(
            self,
            error_topic=error_topic,
            lambda_function=lambda_function,
            proxy=False,
        ).api

    def create_http_api(self, error_topic):
        return well_architected_constructs.api.Api(
            self, 'HttpApiGateway',
            error_topic=error_topic,
            api_gateway_service_role=False,
            api=aws_cdk.aws_apigatewayv2_alpha.HttpApi(
                self, 'HttpApi',
            )
        ).api

    def create_lambda_function(self, handler_name):
        return well_architected_constructs.lambda_function.LambdaFunctionConstruct(
            self, handler_name,
            error_topic=self.error_topic,
            function_name="lambda_single_purpose",
            handler_name=handler_name,
        ).lambda_function