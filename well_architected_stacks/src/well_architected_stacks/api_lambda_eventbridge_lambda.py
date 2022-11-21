import aws_cdk
import constructs
import well_architected_constructs

from . import well_architected_stack


class ApiLambdaEventBridgeLambda(well_architected_stack.Stack):

    def __init__(self, scope: constructs.Construct, id: str,
        create_http_api=None,
        create_rest_api=None,
        lambda_directory=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.lambda_directory = lambda_directory
        self.approved_transaction = self.create_lambda_construct(
            handler_name="approved_transaction_handler",
            function_name="atm_consumer",
            event_bridge_rule=self.create_event_bridge_rule(
                rule_name="approved_transactions_rule",
                description='Approved Transaction',
                detail={
                    "result": ["approved"]
                }
            ),
        )

        self.ny_prefix_transaction = self.create_lambda_construct(
            handler_name="ny_prefix_transaction_handler",
            function_name="atm_consumer",
            event_bridge_rule=self.create_event_bridge_rule(
                rule_name="ny_prefix_transactions_rule",
                detail={
                    "location": [{"prefix": "NY-"}]
                }
            ),
        )

        self.not_approved_transaction = self.create_lambda_construct(
            handler_name="not_approved_transaction_handler",
            function_name="atm_consumer",
            event_bridge_rule=self.create_event_bridge_rule(
                rule_name="not_approved_transaction_rule",
                detail={
                    "result": [{"anything-but": "approved"}]
                }
            ),
        )

        self.atm_producer = well_architected_constructs.api_lambda.ApiLambda(
            self, 'AtmProducer',
            function_name='atm_producer',
            create_http_api=create_http_api,
            create_rest_api=create_rest_api,
            lambda_directory=lambda_directory,
            error_topic=self.error_topic,
        )

        self.atm_producer.lambda_function.add_to_role_policy(
            aws_cdk.aws_iam.PolicyStatement(
                effect=aws_cdk.aws_iam.Effect.ALLOW,
                resources=['*'],
                actions=['events:PutEvents']
            )
        )

        self.create_cloudwatch_dashboard(
            *self.approved_transaction.create_cloudwatch_widgets(),
            *self.ny_prefix_transaction.create_cloudwatch_widgets(),
            *self.not_approved_transaction.create_cloudwatch_widgets(),
            *self.atm_producer.lambda_construct.create_cloudwatch_widgets(),
            *self.atm_producer.api_construct.create_cloudwatch_widgets(),
        )

    def create_event_bridge_rule(self, rule_name=None, description=None, detail=None):
        return aws_cdk.aws_events.Rule(
            self, rule_name,
            description=description,
            event_pattern=aws_cdk.aws_events.EventPattern(
                source=['custom.myATMapp'],
                detail_type=['transaction'],
                detail=detail
            )
        )

    def create_lambda_construct(
        self, handler_name='handler', function_name=None,
        event_bridge_rule:aws_cdk.aws_events.Rule=None,
    ):
        return well_architected_constructs.lambda_function.LambdaFunction(
            self, handler_name,
            handler_name=handler_name,
            function_name=function_name,
            event_bridge_rule=event_bridge_rule,
            error_topic=self.error_topic,
            lambda_directory=self.lambda_directory,
        )
