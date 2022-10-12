import aws_cdk
import constructs
import well_architected_constructs

from . import well_architected_stack


class ApiLambdaSqsLambdaDynamodb(well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        create_http_api=None,
        create_rest_api=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        self.create_error_topic()

        sqs_queue = aws_cdk.aws_sqs.Queue(
            self, 'SqsQueue',
            visibility_timeout=aws_cdk.Duration.seconds(300)
        )

        # dynamodb_table = self.create_dynamodb_table(
        #     partition_key="id",
        # )
        # self.create_sqs_subscribing_lambda(
        #     sqs_queue=sqs_queue,
        #     dynamodb_table=dynamodb_table,
        # )

        sqs_subscriber = well_architected_constructs.api_lambda_dynamodb.ApiLambdaDynamodbConstruct(
            self, 'LambdaDynamodb',
            function_name='api_lambda_sqs_lambda_dynamodb_subscriber',
            partition_key="id",
            lambda_directory=self.lambda_directory,
            concurrent_executions=2,
            environment_variables={
                'SQS_QUEUE_URL': sqs_queue.queue_url,
            },
        )
        
        sqs_publishing_lambda = self.create_sqs_publishing_lambda(sqs_queue)
        self.create_cloudwatch_dashboard(

        )


    def create_dynamodb_table(self, partition_key):
        return well_architected_constructs.dynamodb_table.DynamodbTableConstruct(
            self, "DynamodbTable",
            partition_key=partition_key,
            error_topic=self.error_topic,
        ).dynamodb_table

    def create_lambda_function(
        self, function_name=None,
        environment_variables=None, concurrent_executions=None,
    ):
        return well_architected_constructs.lambda_function.create_python_lambda_function(
            self, function_name=function_name,
            environment_variables=environment_variables,
            concurrent_executions=concurrent_executions,
            error_topic=self.error_topic,
            lambda_directory=self.lambda_directory,
        )

    def create_sqs_publishing_lambda(
        self, sqs_queue:aws_cdk.aws_sqs.Queue
    ):
        lambda_construct = self.create_lambda_function(
            function_name='api_lambda_sqs_lambda_dynamodb_publisher',
            environment_variables={
                'SQS_QUEUE_URL': sqs_queue.queue_url
            },
        )
        lambda_function = lambda_construct.lambda_function
        sqs_queue.grant_send_messages(lambda_function)
        return lambda_function

    def create_sqs_subscribing_lambda(
        self, sqs_queue: aws_cdk.aws_sqs.Queue=None,
        dynamodb_table:aws_cdk.aws_dynamodb.Table=None,
    ):
        lambda_construct = self.create_lambda_function(
            function_name='api_lambda_sqs_lambda_dynamodb_subscriber',
            concurrent_executions=2,
            environment_variables={
                'SQS_QUEUE_URL': sqs_queue.queue_url,
                'DYNAMODB_TABLE_NAME': dynamodb_table.table_name
            },
        )
        lambda_function = lambda_construct.lambda_function
        lambda_function.add_event_source(aws_cdk.aws_lambda_event_sources.SqsEventSource(sqs_queue))
        sqs_queue.grant_consume_messages(lambda_function)
        dynamodb_table.grant_read_write_data(lambda_function)
        return lambda_function
