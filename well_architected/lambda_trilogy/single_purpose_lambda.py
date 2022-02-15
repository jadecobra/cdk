from aws_cdk import (
    aws_lambda as aws_lambda,
    aws_apigateway as api_gw,
    core as cdk
)


class TheSinglePurposeFunctionStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ###
        # We have 3 separate lambda functions, all coming from separate files
        ###

        add_lambda = aws_lambda.Function(
            self, "addLambdaHandler",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            handler="add.handler",
            code=aws_lambda.Code.from_asset("lambda_functions/single_purpose_lambda")
        )

        subtract_lambda = aws_lambda.Function(
            self, "subtractLambdaHandler",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            handler="subtract.handler",
            code=aws_lambda.Code.from_asset("lambda_functions/single_purpose_lambda")
        )

        multiply_lambda = aws_lambda.Function(
            self, "multiplyLambdaHandler",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            handler="multiply.handler",
            code=aws_lambda.Code.from_asset("lambda_functions/single_purpose_lambda")
        )

        ###
        # All functions have their own endpoint defined on our gateway
        ##

        api = api_gw.LambdaRestApi(
            self, 'singlePurposeFunctionAPI',
            handler=add_lambda,
            proxy=False
        )

        api.root.resource_for_path('add').add_method('GET', api_gw.LambdaIntegration(add_lambda))
        api.root.resource_for_path('subtract').add_method('GET', api_gw.LambdaIntegration(subtract_lambda))
        api.root.resource_for_path('multiply').add_method('GET', api_gw.LambdaIntegration(multiply_lambda))

    def create_lambda_function(self, logical_name=None, function_name=None):
        return aws_lambda.Function(
            self, logical_name,
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            handler=f"{function_name}.handler",
            code=aws_lambda.Code.from_asset("lambda_functions/single_purpose_lambda")
        )