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
        sqs_queue = sqs.Queue(self, 'RDSPublishQueue', visibility_timeout=cdk.Duration.seconds(300))

        # defines an AWS  Lambda resource to publish to our sqs_queue
        sqs_publishaws_lambda = aws_lambda.Function(
            self, "SQSPublishLambdaHandler",
            runtime=aws_lambda.Runtime.NODEJS_12_X,
            handler="lambda.handler",
            code=aws_lambda.Code.from_asset("lambda_functions/publish"),
            environment={
                'queueURL': sqs_queue.queue_url
            }
        )
        sqs_queue.grant_send_messages(sqs_publishaws_lambda)

        # defines an AWS  Lambda resource to pull from our sqs_queue
        sqs_subscribeaws_lambda = aws_lambda.Function(
            self, "SQSSubscribeLambdaHandler",
            runtime=aws_lambda.Runtime.NODEJS_12_X,
            handler="lambda.handler",
            code=aws_lambda.Code.from_asset("lambda_functions/subscribe"),
            environment={
                'queueURL': sqs_queue.queue_url,
                'tableName': table.table_name
            },
            reserved_concurrent_executions=2
        )
        sqs_queue.grant_consume_messages(sqs_subscribeaws_lambda)
        sqs_subscribeaws_lambda.add_event_source(lambda_event.SqsEventSource(sqs_queue))
        table.grant_read_write_data(sqs_subscribeaws_lambda)

        api_gw.LambdaRestApi(
            self, 'Endpoint',
            handler=sqs_publishaws_lambda
        )
