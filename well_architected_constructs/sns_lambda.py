import aws_cdk
import constructs
import well_architected
import well_architected_constructs.lambda_function


class SnsLambdaConstruct(well_architected.Construct):

    def __init__(
        self, scope: constructs.Construct, id: str,
        sns_topic: aws_cdk.aws_sns.Topic=None,
        error_topic=None,
        function_name=None,
        **kwargs
    ) -> None:
        super().__init__(
            scope, id,
            error_topic=error_topic,
            **kwargs
        )

        self.lambda_function = well_architected_constructs.lambda_function.create_python_lambda_function(
            scope,
            function_name=function_name,
            error_topic=error_topic,
        )
        sns_topic.add_subscription(
            aws_cdk.aws_sns_subscriptions.LambdaSubscription(
                self.lambda_function
            )
        )