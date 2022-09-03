import constructs
import well_architected_constructs

from . import well_architected_stack


class ApiLambdaDynamodbStack(well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        lambda_directory=None,
        function_name=None,
        partition_key=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        self.lambda_function = well_architected_constructs.api_lambda_dynamodb.ApiLambdaDynamodbConstruct(
            self, 'ApiLambdaDynamodb',
            lambda_directory=lambda_directory,
            function_name=function_name,
            error_topic=self.error_topic,
            partition_key=partition_key,
        ).lambda_function

    def create_http_api_lambda(self):
        return well_architected_constructs.api_lambda.create_http_api_lambda(
            self, lambda_function=self.lambda_function,
            error_topic=self.error_topic,
        )

    def create_rest_api_lambda(self):
        return well_architected_constructs.api_lambda.create_rest_api_lambda(
            self, lambda_function=self.lambda_function,
            error_topic=self.error_topic,
        )