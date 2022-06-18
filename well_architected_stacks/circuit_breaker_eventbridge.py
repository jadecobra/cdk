from distutils.log import error
import aws_cdk
import constructs
import well_architected
import well_architected_constructs.api_lambda
import well_architected_constructs.lambda_function
import well_architected_constructs.dynamodb_table

class CircuitBreakerEventBridge(well_architected.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        dynamodb_table = self.create_dynamodb_table()

        dynamodb_table.add_global_secondary_index(
            index_name='UrlIndex',
            partition_key=aws_cdk.aws_dynamodb.Attribute(
                name="SiteUrl",
                type=aws_cdk.aws_dynamodb.AttributeType.STRING
            ),
            sort_key=self.get_sort_key(),
        )

        lambda_function = well_architected_constructs.lambda_function.create_python_lambda_function(
            self, function_name='webservice',
            error_topic=self.error_topic,
            environment_variables=dict(ERROR_RECORDS=dynamodb_table.table_name),
            duration=20,
        )

        error_lambda = well_architected_constructs.lambda_function.create_python_lambda_function(
            self, function_name='error',
            error_topic=self.error_topic,
            environment_variables=dict(ERROR_RECORDS=dynamodb_table.table_name),
            duration=3,
        )

        dynamodb_table.grant_read_data(lambda_function)
        dynamodb_table.grant_write_data(error_lambda)

        lambda_function.add_to_role_policy(
            aws_cdk.aws_iam.PolicyStatement(
                effect=aws_cdk.aws_iam.Effect.ALLOW,
                resources=['*'],
                actions=['events:PutEvents']
            )
        )

        error_rule = aws_cdk.aws_events.Rule(
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

        error_rule.add_target(
            aws_cdk.aws_events_targets.LambdaFunction(error_lambda)
        )

        well_architected_constructs.api_lambda.create_http_api_lambda(
            self,
            lambda_function=lambda_function,
            error_topic=self.error_topic
        )
        well_architected_constructs.api_lambda.create_rest_api_lambda(
            self,
            lambda_function=lambda_function,
            error_topic=self.error_topic
        )

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