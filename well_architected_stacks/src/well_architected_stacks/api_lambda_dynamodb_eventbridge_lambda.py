import aws_cdk
import constructs
import well_architected_constructs

from . import well_architected_stack


class ApiLambdaDynamodbEventBridgeLambda(well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        self.create_error_topic()
        self.dynamodb_table = self.create_dynamodb_table()
        self.add_global_secondary_index(self.dynamodb_table)
        self.error_handler = self.create_error_handling_lambda_function(self.dynamodb_table)
        self.webservice_lambda_function = self.create_webservice_lambda_function(self.dynamodb_table)

        self.http_api = well_architected_constructs.api_lambda.create_http_api_lambda(
            self,
            lambda_function=self.webservice_lambda_function,
            error_topic=self.error_topic
        )
        self.rest_api = well_architected_constructs.api_lambda.create_rest_api_lambda(
            self,
            lambda_function=self.webservice_lambda_function,
            error_topic=self.error_topic
        )

        self.create_cloudwatch_dashboard(
            *self.dynamodb_table.create_cloudwatch_widgets(),
            *self.webservice_lambda_function.create_cloudwatch_widgets(),
            *self.error_handler.create_cloudwatch_widgets(),
            *self.http_api.create_cloudwatch_widgets(),
            *self.rest_api.create_cloudwatch_widgets(),
        )

    def create_lambda_function(
        self, function_name=None, dynamodb_table_name=None,
        duration=None,
        event_bridge_rule=None,
    ):
        return well_architected_constructs.lambda_function.create_python_lambda_function(
            self, function_name=function_name,
            lambda_directory=self.lambda_directory,
            error_topic=self.error_topic,
            environment_variables=dict(DYNAMODB_TABLE_NAME=dynamodb_table_name),
            duration=duration,
            event_bridge_rule=event_bridge_rule,
        )

    def create_webservice_lambda_function(
        self, dynamodb_table:aws_cdk.aws_dynamodb.Table,
    ):
        lambda_function = self.create_lambda_function(
            function_name='webservice',
            dynamodb_table_name=dynamodb_table.table_name,
            duration=20,
        )
        lambda_function.add_to_role_policy(
            aws_cdk.aws_iam.PolicyStatement(
                effect=aws_cdk.aws_iam.Effect.ALLOW,
                resources=['*'],
                actions=['events:PutEvents']
            )
        )
        dynamodb_table.grant_read_data(lambda_function)
        return lambda_function

    def create_event_bridge_rule(self):
        return aws_cdk.aws_events.Rule(
            self, 'webserviceErrorRule',
            description='Failed Webservice Call',
            event_pattern=aws_cdk.aws_events.EventPattern(
                source=['cdkpatterns.eventbridge.circuitbreaker'],
                detail_type=['httpcall'],
                detail={
                    "status": ["fail"]
                }
            )
        )

    def create_error_handling_lambda_function(
        self, dynamodb_table:aws_cdk.aws_dynamodb.Table,
    ):
        return well_architected_constructs.api_lambda_dynamodb.ApiLambdaDynamodbConstruct(
            self, 'LambdaDynamodb',
            function_name='error',
            # dynamodb_table_name=dynamodb_table.table_name,
            partition_key="RequestID",
            sort_key=self.get_sort_key(),
            duration=3,
            event_bridge_rule=self.create_event_bridge_rule()
            error_topic=self.error_topic,
            time_to_live_attribute='ExpirationTime',
        )
        lambda_construct = self.create_lambda_function(
            function_name='error',
            dynamodb_table_name=dynamodb_table.table_name,
            duration=3,
            event_bridge_rule=aws_cdk.aws_events.Rule(
                self, 'webserviceErrorRule',
                description='Failed Webservice Call',
                event_pattern=aws_cdk.aws_events.EventPattern(
                    source=['cdkpatterns.eventbridge.circuitbreaker'],
                    detail_type=['httpcall'],
                    detail={
                        "status": ["fail"]
                    }
                )
            )
        )
        dynamodb_table.grant_write_data(lambda_construct.lambda_function)
        return lambda_construct

    @staticmethod
    def get_sort_key():
        return aws_cdk.aws_dynamodb.Attribute(
            name="ExpirationTime",
            type=aws_cdk.aws_dynamodb.AttributeType.NUMBER
        )

    def create_dynamodb_table(self):
        return well_architected_constructs.dynamodb_table.DynamodbTableConstruct(
            self, 'CircuitBreaker',
            error_topic=self.error_topic,
            partition_key="RequestID",
            sort_key=self.get_sort_key(),
            time_to_live_attribute='ExpirationTime',
        ).dynamodb_table

    def add_global_secondary_index(self, dynamodb_table):
        return dynamodb_table.add_global_secondary_index(
            index_name='UrlIndex',
            partition_key=aws_cdk.aws_dynamodb.Attribute(
                name="SiteUrl",
                type=aws_cdk.aws_dynamodb.AttributeType.STRING
            ),
            sort_key=self.get_sort_key(),
        )