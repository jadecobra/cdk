from aws_cdk import (
    aws_lambda as aws_lambda,
    aws_lambda_event_sources as lambda_event,
    aws_apigateway as api_gw,
    aws_dynamodb as dynamo_db,
    aws_sqs as sqs,
    core as cdk
)


class ScalableWebhook(cdk.Stack):
    '''This pattern is made obsolete by RDS Proxy'''

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # DynamoDB Table
        # This is standing in for what is RDS on the diagram due to simpler/cheaper setup
        table = dynamo_db.Table(
            self, "Messages",
            partition_key=dynamo_db.Attribute(name="id", type=dynamo_db.AttributeType.STRING)
        )

        # Queue Setup
        queue = sqs.Queue(self, 'RDSPublishQueue', visibility_timeout=cdk.Duration.seconds(300))

        # defines an AWS  Lambda resource to publish to our sqs_queue
        # publisher = aws_lambda.Function(
        #     self, "SQSPublishLambdaHandler",
        #     runtime=aws_lambda.Runtime.NODEJS_12_X,
        #     handler="lambda.handler",
        #     code=aws_lambda.Code.from_asset("lambda_functions/publish"),
        #     environment={
        #         'queueURL': queue.queue_url
        #     }
        # )
        publisher = self.create_lambda_function(
            stack_name="SQSPublishLambdaHandler",
            function_name='publish',
            environment_variables={
                'queueURL': queue.queue_url
            }
        )
        queue.grant_send_messages(publisher)

        # defines an AWS  Lambda resource to pull from our sqs_queue
        subscriber = aws_lambda.Function(
            self, "SQSSubscribeLambdaHandler",
            runtime=aws_lambda.Runtime.NODEJS_12_X,
            handler="lambda.handler",
            code=aws_lambda.Code.from_asset("lambda_functions/subscribe"),
            environment={
                'queueURL': queue.queue_url,
                'tableName': table.table_name
            },
            reserved_concurrent_executions=2
        )
        queue.grant_consume_messages(subscriber)
        subscriber.add_event_source(lambda_event.SqsEventSource(queue))
        table.grant_read_write_data(subscriber)

        api_gw.LambdaRestApi(
            self, 'Endpoint',
            handler=publisher
        )

    def create_lambda_function(self, stack_name=None, environment_variables=None, function_name=None):
        return aws_lambda.Function(
            self, stack_name,
            runtime=aws_lambda.Runtime.NODEJS_12_X,
            handler="lambda.handler",
            code=aws_lambda.Code.from_asset(f"lambda_functions/{function_name}"),
            environment=environment_variables
        )
