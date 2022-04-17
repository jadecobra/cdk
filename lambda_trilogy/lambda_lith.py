import aws_cdk
import constructs
import lambda_function
import rest_api

from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as api_gw,
)

class LambdaLith(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        rest_api.LambdaRestAPIGatewayConstruct(
            self, 'LambdaLithRestAPIGateway',
            lambda_function=lambda_function.create_python_lambda_function(
                self, function_name='lambdalith'
            ),
        )