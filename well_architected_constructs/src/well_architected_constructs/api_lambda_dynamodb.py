from time import time
import constructs

from . import api_lambda
from . import dynamodb_table
from . import lambda_function
from . import well_architected_construct


class ApiLambdaDynamodbConstruct(well_architected_construct.Construct):

    def __init__(
        self, scope: constructs.Construct, id: str,
        function_name=None,
        partition_key=None,
        error_topic=None,
        lambda_directory=None,
        duration=60,
        event_bridge_rule=None,
        time_to_live_attribute=None,
        sort_key=None,
        **kwargs
    ) -> None:
        super().__init__(
            scope, id,
            error_topic=error_topic,
            **kwargs
        )
        self.dynamodb_table = dynamodb_table.DynamodbTableConstruct(
            self, 'DynamoDbTable',
            partition_key=partition_key,
            sort_key=sort_key,
            time_to_live_attribute=time_to_live_attribute,
            error_topic=error_topic,
        )
        self.lambda_function = self.create_lambda_function(
            dynamodb_table_name=self.dynamodb_table.dynamodb_table.table_name,
            lambda_directory=lambda_directory,
            function_name=function_name,
            duration=duration,
            error_topic=error_topic,
            event_bridge_rule=event_bridge_rule,
        )
        self.dynamodb_table.dynamodb_table.grant_read_write_data(
            self.lambda_function.lambda_function
        )

    def create_lambda_function(
        self,
        dynamodb_table_name=None,
        function_name=None,
        lambda_directory=None,
        duration=None,
        error_topic=None,
        event_bridge_rule=None,
    ):
        return lambda_function.LambdaFunctionConstruct(
            self, 'LambdaFunction',
            error_topic=error_topic,
            event_bridge_rule=event_bridge_rule,
            function_name=function_name,
            duration=duration,
            lambda_directory=lambda_directory,
            environment_variables={
                'DYNAMODB_TABLE_NAME': dynamodb_table_name
            }
        )

    def create_http_api_lambda(self):
        return api_lambda.create_http_api_lambda(
            self, lambda_function=self.lambda_function.lambda_function,
            error_topic=self.error_topic,
        )

    def create_rest_api_lambda(self):
        return api_lambda.create_rest_api_lambda(
            self, lambda_function=self.lambda_function.lambda_function,
            error_topic=self.error_topic,
        )