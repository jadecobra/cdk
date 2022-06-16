import constructs
import well_architected
import well_architected_constructs.api
import well_architected_constructs.api_lambda
import well_architected_constructs.dynamodb_table
import well_architected_constructs.lambda_function


class ApiLambdaDynamodb(well_architected.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        function_name=None, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        dynamodb_table = self.create_dynamodb_table(id)
        lambda_function = self.create_lambda_function(
            dynamodb_table_name=dynamodb_table.table_name,
            function_name=function_name,
        )
        dynamodb_table.grant_read_write_data(lambda_function)

        well_architected_constructs.api_lambda.create_http_api_lambda(
            self, lambda_function=lambda_function
        )
        well_architected_constructs.api_lambda.create_rest_api_lambda(
            self, lambda_function=lambda_function
        )

    def create_dynamodb_table(self, id):
        return well_architected_constructs.dynamodb_table.DynamoDBTableConstruct(
            self, 'DynamoDbTable',
            partition_key="id",
            error_topic=self.error_topic,
        ).dynamodb_table

    def create_lambda_function(self, dynamodb_table_name=None, function_name=None):
        return well_architected_constructs.lambda_function.LambdaFunctionConstruct(
            self, 'LambdaFunction',
            error_topic=self.error_topic,
            function_name=function_name,
            environment_variables={
                'DYNAMODB_TABLE_NAME': dynamodb_table_name
            }
        ).lambda_function