from venv import create
import constructs
import well_architected_constructs

from . import well_architected_stack


class ApiLambdaDynamodbStack(well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        function_name=None,
        partition_key=None,
        create_http_api=False,
        create_rest_api=False,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        self.create_error_topic()
        self.api_lambda_dynamodb = well_architected_constructs.api_lambda_dynamodb.ApiLambdaDynamodbConstruct(
            self, 'ApiLambdaDynamodb',
            lambda_directory=self.lambda_directory,
            function_name=function_name,
            error_topic=self.error_topic,
            partition_key=partition_key,
            create_http_api=create_http_api,
            create_rest_api=create_rest_api,
        )
        self.create_cloudwatch_dashboard()

    def create_cloudwatch_dashboard(self):
        return self.create_cloudwatch_dashboard(
            *self.api_lambda_dynamodb.create_cloudwatch_widgets(),
            *self.api.create_cloudwatch_widgets(),
        )
        self.create_cloudwatch_dashboard(
            *self.api_lambda_dynamodb.lambda_function.create_cloudwatch_widgets(),
            *self.api_lambda_dynamodb.dynamodb_table.create_cloudwatch_widgets(),
        )
