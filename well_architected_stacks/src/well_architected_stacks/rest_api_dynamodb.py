import aws_cdk
import constructs
import json
import well_architected_constructs

from . import well_architected_stack


class RestApiDynamodb(well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        partition_key:str,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        self.create_error_topic()

        self.dynamodb_table_construct = self.create_dynamodb_table(partition_key)
        self.dynamodb_table = self.dynamodb_table_construct.dynamodb_table
        self.lambda_construct =well_architected_constructs.lambda_function.LambdaFunction(
            self, 'LambdaFunction',
            function_name='subscribe',
            error_topic=self.error_topic,
            lambda_directory=self.lambda_directory,
        )
        self.add_dynamodb_event_source(
            lambda_function=self.lambda_construct.lambda_function,
            dynamodb_table=self.dynamodb_table,
        )

        self.rest_api_construct = self.create_rest_api_construct(self.error_topic)

        self.create_api_dynamodb_integration(
            rest_api=self.rest_api_construct,
            request_templates=self.get_request_template(self.dynamodb_table.table_name),
            partition_key=partition_key,
        )
        self.dynamodb_table.grant_read_write_data(
            self.rest_api_construct.api_gateway_service_role
        )

        self.create_cloudwatch_dashboard(
            *self.rest_api_construct.create_cloudwatch_widgets(),
            *self.dynamodb_table_construct.create_cloudwatch_widgets(),
            *self.lambda_construct.create_cloudwatch_widgets(),
        )

    def create_rest_api_construct(self, error_topic):
        return well_architected_constructs.rest_api.RestApi(
            self, 'RestApiDynamodb',
            error_topic=error_topic,
        )


    def create_api_dynamodb_integration(
        self, rest_api=None, request_templates=None, partition_key=None
    ):
        return rest_api.add_method(
            method='POST',
            path='InsertItem',
            uri='arn:aws:apigateway:us-east-1:dynamodb:action/PutItem',
            request_templates=request_templates,
            error_selection_pattern="BadRequest",
            success_response_templates={
                partition_key: 'item added to db'
            },
        )

    def get_request_template(self, table_name):
        return json.dumps({
            "TableName": table_name,
            "Item": {
                "message": { "S": "$input.path('$.message')" }
            }
        })

    def create_dynamodb_table(self, partition_key):
        return well_architected_constructs.dynamodb_table.DynamodbTable(
            self, 'DynamoDbTable',
            stream=aws_cdk.aws_dynamodb.StreamViewType.NEW_IMAGE,
            error_topic=self.error_topic,
            partition_key=partition_key,
        )

    @staticmethod
    def add_dynamodb_event_source(lambda_function=None, dynamodb_table=None):
        return lambda_function.add_event_source(
            aws_cdk.aws_lambda_event_sources.DynamoEventSource(
                table=dynamodb_table,
                starting_position=aws_cdk.aws_lambda.StartingPosition.LATEST,
            )
        )