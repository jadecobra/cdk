from aws_cdk import (
    aws_lambda,
    aws_apigateway as api_gateway,
    aws_events as events,
    aws_events_targets as targets,
    aws_iam as iam,
    core as cdk
)


class EventBridgeAtm(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        approved_transaction_rule = self.create_event_bridge_rule(
            rule_name='atm_consumer1LambdaRule',
            description='Approved Transactions',
            detail={
                "result": ["approved"]
            }
        )

        ny_prefix_transaction_rule = self.create_event_bridge_rule(
            rule_name='atm_consumer2LambdaRule',
            detail={
                "location": [{"prefix": "NY-"}]
            }
        )

        not_approved_transaction_rule = self.create_event_bridge_rule(
            rule_name='atm_consumer3LambdaRule',
            detail={
                "result": [{"anything-but": "approved"}]
            }
        )

        self.create_lambda_function(
            stack_name="atm_consumer1Lambda",
            handler_name="case_1_handler",
            function_name="atm_consumer",
            event_bridge_rule=approved_transaction_rule,
        )

        self.create_lambda_function(
            stack_name="atm_consumer2Lambda",
            handler_name="case_2_handler",
            function_name="atm_consumer",
            event_bridge_rule=ny_prefix_transaction_rule,
        )

        self.create_lambda_function(
            stack_name="atm_consumer3Lambda",
            handler_name="case_3_handler",
            function_name="atm_consumer",
            event_bridge_rule=not_approved_transaction_rule,
        )

        atm_producer_lambda = self.create_lambda_function(
            stack_name="atmProducerLambda",
            handler_name="lambdaHandler",
            function_name="atm_producer"
        )

        atm_producer_lambda.add_to_role_policy(
                iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                resources=['*'],
                actions=['events:PutEvents']
            )
        )

        api_gateway.LambdaRestApi(
            self, 'Endpoint',
            handler=atm_producer_lambda
        )

    def create_event_bridge_rule(self, rule_name=None, description=None, detail=None):
        return events.Rule(
            self, rule_name,
            description=description,
            event_pattern=events.EventPattern(
                source=['custom.myATMapp'],
                detail_type=['transaction'],
                detail=detail
            )
        )

    def create_lambda_function(
        self, stack_name=None, handler_name=None, function_name=None,
        event_bridge_rule:events.Rule=None
    ):
        lambda_function = aws_lambda.Function(
            self, stack_name,
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler=f"handler.{handler_name}",
            code=aws_lambda.Code.from_asset(f"lambda_functions/{function_name}")
        )
        if event_bridge_rule:
            event_bridge_rule.add_target(
                targets.LambdaFunction(
                    handler=lambda_function
                )
            )
        return lambda_function
