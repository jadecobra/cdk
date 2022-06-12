import aws_cdk
import constructs
import well_architected
import well_architected_constructs.lambda_function
import well_architected_constructs.sns_lambda


class SnsLambda(well_architected.Stack):

    def __init__(
        self, scope: constructs.Construct,
        id: str,
        sns_topic: aws_cdk.aws_sns.ITopic=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        well_architected_constructs.sns_lambda.SnsLambdaConstruct(
            self, "SnsLambda",
            function_name="sns_lambda",
            sns_topic=sns_topic,
            error_topic=self.error_topic,
        )
        # sns_topic.add_subscription(
        #     aws_cdk.aws_sns_subscriptions.LambdaSubscription(
        #         well_architected_constructs.lambda_function.create_python_lambda_function(
        #             self,
        #             function_name="sns_lambda",
        #         )
        #     )
        # )