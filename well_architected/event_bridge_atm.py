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



        #
        # Approved Transaction Consumer
        #
        atm_consumer1_lambda = aws_lambda.Function(
            self, "atm_consumer1Lambda",
            runtime=aws_lambda.Runtime.NODEJS_12_X,
            handler="handler.case_1_handler",
            code=aws_lambda.Code.from_asset("lambda_functions/atm_consumer")
        )

        atm_consumer1_rule = events.Rule(
            self, 'atm_consumer1LambdaRule',
            description='Approved Transactions',
            event_pattern=events.EventPattern(
                source=['custom.myATMapp'],
                detail_type=['transaction'],
                detail={
                    "result": ["approved"]
                }
            )
        )


        #
        # NY Prefix Consumer
        #
        atm_consumer2_lambda = aws_lambda.Function(
            self, "atm_consumer2Lambda",
            runtime=aws_lambda.Runtime.NODEJS_12_X,
            handler="handler.case_2_handler",
            code=aws_lambda.Code.from_asset("lambda_functions/atm_consumer")
        )

        atm_consumer2_rule = events.Rule(
            self, 'atm_consumer2LambdaRule',
            event_pattern=events.EventPattern(
                source=['custom.myATMapp'],
                detail_type=['transaction'],
                detail={
                    "location": [{"prefix": "NY-"}]
                }
            )
        )



        #
        # Not Approved Consumer
        #
        atm_consumer3_lambda = aws_lambda.Function(
            self, "atm_consumer3Lambda",
            runtime=aws_lambda.Runtime.NODEJS_12_X,
            handler="handler.case_3_handler",
            code=aws_lambda.Code.from_asset("lambda_functions/atm_consumer")
        )

        atm_consumer3_rule = events.Rule(
            self, 'atm_consumer3LambdaRule',
            event_pattern=events.EventPattern(
                source=['custom.myATMapp'],
                detail_type=['transaction'],
                detail={
                    "result": [{"anything-but": "approved"}]
                }
            )
        )

        atm_consumer1_rule.add_target(targets.LambdaFunction(handler=atm_consumer1_lambda))
        atm_consumer2_rule.add_target(targets.LambdaFunction(handler=atm_consumer2_lambda))
        atm_consumer3_rule.add_target(targets.LambdaFunction(handler=atm_consumer3_lambda))


        atm_producer_lambda = aws_lambda.Function(
            self, "atmProducerLambda",
            runtime=aws_lambda.Runtime.NODEJS_12_X,
            handler="handler.lambdaHandler",
            code=aws_lambda.Code.from_asset("lambda_functions/atm_producer")
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
