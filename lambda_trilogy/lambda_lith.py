import aws_cdk
import constructs
import well_architected
import well_architected_constructs.lambda_function
import well_architected_constructs.rest_api

from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as api_gw,
)

class LambdaLith(well_architected.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        lambda_function = well_architected_constructs.lambda_function.create_python_lambda_function(
                self,
                function_name='lambda_lith'
        )

        well_architected_constructs.api_lambda.create_http_api(
            self, 'LambdaLithRestAPIGateway',
            lambda_function=lambda.create_python_lambda_function(
                self, function_name='lambdalith'
            ),
        )