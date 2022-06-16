import constructs
import well_architected
import well_architected_constructs.api
import well_architected_constructs.api_lambda
import well_architected_constructs.dynamodb_table
import well_architected_constructs.lambda_function
import well_architected_constructs.api_lambda_dynamodb

class ApiLambdaDynamodb(well_architected.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        function_name=None, partition_key=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        well_architected_constructs.api_lambda_dynamodb.ApiLambdaDynamodbConstruct(
            self, 'ApiLambdaDynamodb',
            function_name=function_name,
            error_topic=self.error_topic,
            partition_key=partition_key,
        )