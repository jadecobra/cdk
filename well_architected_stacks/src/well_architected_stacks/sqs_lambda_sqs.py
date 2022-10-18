import aws_cdk
import constructs
import well_architected_constructs

from . import well_architected_stack


class SqsLambdaSqs(well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        sns_topic=None, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.sqs_queue = aws_cdk.aws_sqs.Queue(
            self, 'SqsQueue',
            visibility_timeout=aws_cdk.Duration.seconds(300)
        )
        self.publisher = self.create_sqs_publishing_lambda(
            sqs_queue=self.sqs_queue,
            sns_topic=sns_topic,
        )
        self.subscriber = self.create_sqs_subscribing_lambda(
            sqs_queue=self.sqs_queue,
        )
        self.create_cloudwatch_dashboard(
            *self.publisher.create_cloudwatch_widgets(),
            *self.subscriber.create_cloudwatch_widgets(),
        )

    def create_sqs_publishing_lambda(
        self, sqs_queue: aws_cdk.aws_sqs.Queue=None,
        sns_topic: aws_cdk.aws_sns.Topic=None,
    ):
        sns_lambda = well_architected_constructs.sns_lambda.SnsLambda(
            self, 'SqsPublisher',
            function_name='sqs_publisher',
            lambda_directory=self.lambda_directory,
            error_topic=self.error_topic,
            sns_topic=sns_topic,
            environment_variables={
                'SQS_URL': sqs_queue.queue_url
            }
        )
        sqs_queue.grant_send_messages(sns_lambda.lambda_function)
        return sns_lambda.lambda_construct

    def create_sqs_subscribing_lambda(
        self, sqs_queue: aws_cdk.aws_sqs.Queue=None,
    ):
        lambda_construct = well_architected_constructs.lambda_function.create_python_lambda_function(
            self, function_name="sqs_subscriber",
            lambda_directory=self.lambda_directory,
            error_topic=self.error_topic,
        )
        lambda_construct.lambda_function.add_event_source(
            aws_cdk.aws_lambda_event_sources.SqsEventSource(
                sqs_queue
            )
        )
        sqs_queue.grant_consume_messages(lambda_construct.lambda_function)
        return lambda_construct