import constructs
import well_architected_constructs

from .. import well_architected_stack

class LambdaLith(well_architected_stack.Stack):

    def __init__(self, scope: constructs.Construct, id: str, function_name=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


        self.api_lambda_construct = well_architected_constructs.api_lambda.ApiLambda(
            self, function_name,
            function_name=function_name,
            lambda_directory=self.lambda_directory,
            error_topic=self.error_topic,
            create_http_api=self.create_http_api,
            create_rest_api=self.create_rest_api,
        )

        self.create_cloudwatch_dashboard(
            *self.api_lambda_construct.api_construct.create_cloudwatch_widgets(),
            *self.api_lambda_construct.lambda_construct.create_cloudwatch_widgets(),
        )