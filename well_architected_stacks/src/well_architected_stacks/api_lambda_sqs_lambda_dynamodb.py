import aws_cdk
import constructs
import well_architected_constructs

from . import well_architected_stack


class ApiLambdaSqsLambdaDynamodb(well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)


        sqs_queue = aws_cdk.aws_sqs.Queue(
            self, 'SqsQueue',
            visibility_timeout=aws_cdk.Duration.seconds(300)
        )

        sqs_subscriber = well_architected_constructs.api_lambda_dynamodb.ApiLambdaDynamodb(
            self, 'LambdaDynamodb',
            function_name='api_lambda_sqs_lambda_dynamodb_subscriber',
            partition_key="id",
            lambda_directory=self.lambda_directory,
            error_topic=self.error_topic,
            create_http_api=self.create_http_api,
            create_rest_api=self.create_rest_api,
            concurrent_executions=2,
            environment_variables={
                'SQS_QUEUE_URL': sqs_queue.queue_url,
            },
        )

        sqs_subscriber.lambda_function.add_event_source(aws_cdk.aws_lambda_event_sources.SqsEventSource(sqs_queue))
        sqs_queue.grant_consume_messages(sqs_subscriber.lambda_function)
        sqs_subscriber.dynamodb_table.grant_read_write_data(sqs_subscriber.lambda_function)

        sqs_publisher = self.create_sqs_publishing_lambda(sqs_queue)

        self.create_cloudwatch_dashboard(
            *sqs_subscriber.api_construct.create_cloudwatch_widgets(),
            *sqs_subscriber.lambda_construct.create_cloudwatch_widgets(),
            *sqs_subscriber.dynamodb_construct.create_cloudwatch_widgets(),
            *sqs_publisher.create_cloudwatch_widgets(),
        )

    def create_lambda_construct(
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
        lambda_construct = self.create_lambda_construct(
            function_name='api_lambda_sqs_lambda_dynamodb_publisher',
            environment_variables={
                'SQS_QUEUE_URL': sqs_queue.queue_url
            },
        )
        lambda_function = lambda_construct.lambda_function
        sqs_queue.grant_send_messages(lambda_function)
        return lambda_construct

    def create_sqs_subscribing_lambda(
        self, sqs_queue: aws_cdk.aws_sqs.Queue=None,
        dynamodb_table:aws_cdk.aws_dynamodb.Table=None,
    ):
        lambda_construct = self.create_lambda_construct(
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
