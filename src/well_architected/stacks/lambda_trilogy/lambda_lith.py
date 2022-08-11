import constructs
import well_architected
import well_architected.constructs.lambda_function
import well_architected.constructs.api_lambda


class LambdaLith(well_architected.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        lambda_function = well_architected.constructs.lambda_function.create_python_lambda_function(
                self,
                function_name='lambda_lith'
        )

        well_architected.constructs.api_lambda.create_rest_api_lambda(
            self, error_topic=self.error_topic,
            lambda_function=lambda_function,
        )

        well_architected.constructs.api_lambda.create_http_api_lambda(
            self, error_topic=self.error_topic,
            lambda_function=lambda_function,
        )