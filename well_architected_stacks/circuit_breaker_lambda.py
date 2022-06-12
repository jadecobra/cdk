import constructs
import well_architected
import well_architected_constructs.api
import well_architected_constructs.api_lambda
import well_architected_constructs.dynamodb_table
import well_architected_constructs.lambda_function


class CircuitBreakerLambda(well_architected.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        dynamodb_table = self.create_dynamodb_table(id)
        lambda_function = self.create_lambda_function(dynamodb_table.table_name)
        dynamodb_table.grant_read_write_data(lambda_function)

        well_architected_constructs.api_lambda.create_http_api_lambda(
            self, lambda_function=lambda_function
        )

    def create_dynamodb_table(self, id):
        return well_architected_constructs.dynamodb_table.DynamoDBTableConstruct(
            self, id,
            partition_key="id",
            error_topic=self.error_topic,
        ).dynamodb_table

    def create_lambda_function(self, table_name):
        return well_architected_constructs.lambda_function.LambdaFunctionConstruct(
            self, 'LambdaFunction',
            error_topic=self.error_topic,
            function_name='circuit_breaker_lambda',
            environment_variables={
                'CIRCUITBREAKER_TABLE': table_name
            }
        ).lambda_function