import aws_cdk
import constructs
import well_architected_constructs

from . import well_architected_stack


class SnsLambdaSns(well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        sns_publisher_trigger=None,
        publisher_lambda_name=None,
        subscriber_lambda_name=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.sns_topic = self.create_sns_topic('SnsTopic')

        self.subscriber = self.create_lambda_construct(
            construct_id='SnsSubscriber',
            function_name=subscriber_lambda_name,
            sns_topic=self.sns_topic,
        )

        self.publisher = self.create_lambda_construct(
            construct_id='SnsPublisher',
            function_name=publisher_lambda_name,
            sns_topic=sns_publisher_trigger,
            environment_variables={
                'TOPIC_ARN': self.sns_topic.topic_arn,
            }
        )

        self.sns_topic.grant_publish(self.publisher.lambda_function)

        self.create_cloudwatch_dashboard(
            *self.subscriber.lambda_construct.create_cloudwatch_widgets(),
            *self.publisher.lambda_construct.create_cloudwatch_widgets(),
        )


    def create_lambda_construct(
        self, construct_id=None, function_name=None, sns_topic=None,
        environment_variables=None,
    ):
        return well_architected_constructs.sns_lambda.SnsLambda(
            self, construct_id,
            function_name=function_name,
            lambda_directory=self.lambda_directory,
            sns_topic=sns_topic,
            error_topic=self.error_topic,
            environment_variables=environment_variables,
        )