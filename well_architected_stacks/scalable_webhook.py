import aws_cdk
import constructs
import well_architected
import well_architected_constructs.lambda_function
import well_architected_constructs.api_lambda
import well_architected_constructs.dynamodb_table


class ScalableWebhook(well_architected.Stack):
    '''This pattern is made obsolete by RDS Proxy'''

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        dynamodb_table = self.create_dynamodb_table(
            partition_key="id",
            error_topic=self.error_topic,
        )

        sqs_queue = aws_cdk.aws_sqs.Queue(
            self, 'RDSPublishQueue',
            visibility_timeout=aws_cdk.Duration.seconds(300)
        )

        sqs_publishing_lambda = self.create_lambda_function(
            function_name='publisher',
            environment_variables={
                'queueURL': sqs_queue.queue_url
            }
        )
        sqs_queue.grant_send_messages(sqs_publishing_lambda)

        sqs_subscribing_lambda = self.create_lambda_function(
            function_name='subscriber',
            environment_variables={
                'queueURL': sqs_queue.queue_url,
                'tableName': dynamodb_table.table_name
            },
            concurrent_executions=2
        )
        sqs_subscribing_lambda.add_event_source(aws_cdk.aws_lambda_event_sources.SqsEventSource(sqs_queue))
        sqs_queue.grant_consume_messages(sqs_subscribing_lambda)
        dynamodb_table.grant_read_write_data(sqs_subscribing_lambda)

        well_architected_constructs.api_lambda.create_http_api_lambda(
            self, lambda_function=sqs_publishing_lambda,
            error_topic=self.error_topic,
        )
        well_architected_constructs.api_lambda.create_rest_api_lambda(
            self, lambda_function=sqs_publishing_lambda,
            error_topic=self.error_topic,
        )

    def create_dynamodb_table(self, partition_key=None, error_topic=None):
        return well_architected_constructs.dynamodb_table.DynamodbTableConstruct(
            self, "DynamodbTable",
            partition_key=partition_key,
            error_topic=error_topic,
        ).dynamodb_table

    def create_lambda_function(
        self, function_name=None,
        environment_variables=None, concurrent_executions=None
    ):
        return well_architected_constructs.lambda_function.create_python_lambda_function(
            self, function_name=function_name,
            environment_variables=environment_variables,
            concurrent_executions=concurrent_executions,
        )