import aws_cdk
import constructs
import aws_cdk.aws_apigatewayv2_alpha
import aws_cdk.aws_apigatewayv2_integrations_alpha

import well_architected_constructs

from .. import well_architected_stack


class LambdaTrilogy(well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        function_name=None, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.function_name = function_name
        add = 'add'
        subtract = 'subtract'
        multiply = 'multiply'

        api_lambda_construct = well_architected_constructs.api_lambda.ApiLambda(
            self, self.function_name,
            function_name=function_name,
            handler_name='add',
            error_topic=self.error_topic,
            lambda_directory=self.lambda_directory,
            create_http_api=self.create_http_api,
            create_rest_api=self.create_rest_api,
            proxy=False,
        )

        subtracter = self.create_lambda_construct(subtract)
        multiplier = self.create_lambda_construct(multiply)

        for path, lambda_construct in (
            (
                (add, api_lambda_construct),
                (subtract, subtracter),
                (multiply, multiplier),
            )
        ):
            api_lambda_construct.add_method(
                path=path, lambda_function=lambda_construct.lambda_function
            )

        self.create_cloudwatch_dashboard(
            *api_lambda_construct.api_construct.create_cloudwatch_widgets(),
            *api_lambda_construct.lambda_construct.create_cloudwatch_widgets(),
            *subtracter.create_cloudwatch_widgets(),
            *multiplier.create_cloudwatch_widgets(),
        )

    def create_lambda_construct(self, handler_name):
        return well_architected_constructs.lambda_function.LambdaFunction(
            self, handler_name,
            error_topic=self.error_topic,
            function_name=self.function_name,
            lambda_directory=self.lambda_directory,
            handler_name=handler_name,
        )