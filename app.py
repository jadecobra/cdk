import aws_cdk
import aws_cdk.aws_dynamodb as aws_dynamodb
import os
try:
    import api_dynamodb
    import api_sns_lambda_eventbridge_lambda
    import api_step_functions
    import circuit_breaker_lambda
    import waf_api_lambda_dynamodb
    import lambda_trilogy.fat_lambda
    import lambda_trilogy.single_purpose_lambda
    import lambda_trilogy.lambda_lith
    import big_fan
    import event_bridge_atm
    import circuit_breaker_event_bridge
    import event_bridge_etl
    import lambda_power_tuner
    import rds_proxy
    import scalable_webhook
    import saga_step_function
    import simple_graphql_service
    import sns_topic
    import xray_tracer
    import well_architected_dynamodb_table
    import web_application_firewall
    import well_architected_api
    import well_architected_rest_api
    import well_architected_lambda
except ImportError as error:
    print(error)
    os.system('pip install -r requirements.txt')


class WellArchitected(aws_cdk.App):

    stack_synthesizer = aws_cdk.DefaultStackSynthesizer(
        generate_bootstrap_version_rule=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        # self.create_xray_tracer()

        # big_fan.BigFan(self, "BigFan")

        api_sns_lambda_eventbridge_lambda.ApiSnsLambdaEventBridgeLambda(self, "ApiSnsLambdaEventBridgeLambda")

        # event_bridge_atm.EventBridgeAtm(self, "EventBridgeAtm")
        # event_bridge_circuit_breaker.EventBridgeCircuitBreaker(
        #     self, 'EventBridgeCircuitBreaker',
        # )
        # event_bridge_etl.EventbridgeEtl(self, 'EventBridgeEtl', )

        # lambda_trilogy.lambda_lith.LambdaLith(self, "LambdaLith", )
        # lambda_trilogy.fat_lambda.TheFatLambdaStack(self, "FatLambda", )
        # lambda_trilogy.single_purpose_lambda.TheSinglePurposeFunctionStack(self, "SinglePurposeLambda", )
        circuit_breaker_lambda.CircuitBreakerLambda(self, "CircuitBreakerLambda", )

        saga_step_function.SagaStepFunction(self, "SagaStepFunction",)
        # lambda_power_tuner.LambdaPowerTuner(self, "LambdaPowerTuner", )
        simple_graphql_service.SimpleGraphQlService(self, "SimpleGraphqlService", )
        api_dynamodb.ApiDynamodb(
            self, 'ApiDynamodb',
            partition_key='message',
        )
        api_step_functions.ApiStepFunctions(self, "ApiStepFunctions")
        waf_api_lambda_dynamodb.WafApiLambdaDynamodb(self, 'WafApiLambdaDynamodb')

    def create_xray_tracer(self):
        xray_tracer_sns_topic = sns_topic.SnsTopic(
            self, 'XRayTracerSnsFanOutTopic', display_name='The XRay Tracer Fan Out Topic'
        ).topic
        xray_tracer.sns_rest_api.SnsRestApi(
            self, 'SnsRestApi', sns_topic=xray_tracer_sns_topic
        )
        xray_tracer.sns_flow.SnsFlow(self, 'SnsFlow', sns_topic=xray_tracer_sns_topic)
        xray_tracer.sqs_flow.SqsFlow(self, 'SqsFlow', sns_topic=xray_tracer_sns_topic)
        xray_tracer.http_flow.HttpFlow(self, 'HttpFlow', sns_topic=xray_tracer_sns_topic)
        xray_tracer.dynamodb_flow.DynamoDBFlow(
            self, 'DynamoDBFlow', sns_topic=xray_tracer_sns_topic
        )

WellArchitected().synth()

# TODO
# Refactor Lambda Circuit Breaker
# abstract Lambda Layers to stack