import aws_cdk
import constructs
import aws_cdk.aws_apigatewayv2_alpha
import aws_cdk.aws_apigatewayv2_integrations_alpha

from . import api
from . import lambda_function
from . import well_architected_construct


class ApiLambdaConstruct(well_architected_construct.Construct):

    def __init__(
        self, scope: constructs.Construct, id: str,
        function_name=None,
        error_topic=None,
        lambda_directory=None,
        duration=60,
        event_bridge_rule=None,
        create_http_api=False,
        create_rest_api=False,
        environment_variables=None,
        **kwargs
    ) -> None:
        super().__init__(
            scope, id,
            error_topic=error_topic,
            **kwargs
        )
        self.lambda_construct = lambda_function.LambdaFunctionConstruct(
            self, 'LambdaFunction',
            error_topic=error_topic,
            event_bridge_rule=event_bridge_rule,
            function_name=function_name,
            duration=duration,
            lambda_directory=lambda_directory,
            environment_variables=environment_variables,
        )
        self.lambda_function = self.lambda_construct.lambda_function
        self.api_construct = self.create_api(
            create_http_api=create_http_api,
            create_rest_api=create_rest_api,
            lambda_function=self.lambda_function,
            error_topic=error_topic,
        )

    def create_api(self,
        create_http_api=None, create_rest_api=None,
        lambda_function=None, error_topic=None
    ):
        if create_http_api:
            return self.create_http_api_lambda(
                lambda_function=lambda_function,
                error_topic=error_topic
            )
        if create_rest_api:
            return self.create_rest_api_lambda(
                lambda_function=lambda_function,
                error_topic=error_topic
            )

    def create_http_api_lambda(
        self, error_topic=None, lambda_function=None
    ):
        return api.Api(
            self, 'HttpApiGateway',
            error_topic=error_topic,
            api_gateway_service_role=False,
            api=aws_cdk.aws_apigatewayv2_alpha.HttpApi(
                self, 'HttpApi',
                default_integration=aws_cdk.aws_apigatewayv2_integrations_alpha.HttpLambdaIntegration(
                    'HttpApiLambdaFunction',
                    handler=lambda_function
                ),
            )
        )

    def create_rest_api_lambda(
        self, error_topic=None, lambda_function=None,
        proxy=True
    ):
        return api.Api(
            self, 'RestApiGateway',
            error_topic=error_topic,
            api_gateway_service_role=False,
            api=aws_cdk.aws_apigateway.LambdaRestApi(
                self, 'RestApiLambdaFunction',
                handler=lambda_function,
                proxy=proxy,
            )
        )

def create_http_api_lambda(
    stack, error_topic=None, lambda_function=None
):
    return api.Api(
        stack, 'HttpApiGateway',
        error_topic=error_topic,
        api_gateway_service_role=False,
        api=aws_cdk.aws_apigatewayv2_alpha.HttpApi(
            stack, 'HttpApi',
            default_integration=aws_cdk.aws_apigatewayv2_integrations_alpha.HttpLambdaIntegration(
                'HttpApiLambdaFunction',
                handler=lambda_function
            ),
        )
    )

def create_rest_api_lambda(
    stack, error_topic=None, lambda_function=None,
    proxy=True
):
    return api.Api(
        stack, 'RestApiGateway',
        error_topic=error_topic,
        api_gateway_service_role=False,
        api=aws_cdk.aws_apigateway.LambdaRestApi(
            stack, 'RestApiLambdaFunction',
            handler=lambda_function,
            proxy=proxy,
        )
    )
