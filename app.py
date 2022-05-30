import aws_cdk

import well_architected_stacks.rest_api_sns_sqs_lambda
import well_architected_stacks.rest_api_sns_lambda_eventbridge_lambda
import well_architected_stacks.rest_api_dynamodb
import well_architected_stacks.simple_graphql_service.simple_graphql_service
import well_architected_stacks.api_step_functions
import well_architected_stacks.circuit_breaker_lambda
import well_architected_stacks.waf_api_lambda_dynamodb


class WellArchitected(aws_cdk.App):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.create_xray_tracer()

        well_architected_stacks.api_step_functions.ApiStepFunctions(self, "ApiStepFunctions")
        well_architected_stacks.circuit_breaker_lambda.CircuitBreakerLambda(self, "CircuitBreakerLambda")
        well_architected_stacks.rest_api_sns_sqs_lambda.ApiSnsSqsLambda(self, 'ApiSnsSqsLambda')
        well_architected_stacks.rest_api_sns_lambda_eventbridge_lambda.ApiSnsLambdaEventBridgeLambda(self, "ApiSnsLambdaEventBridgeLambda")
        well_architected_stacks.rest_api_dynamodb.RestApiDynamodb(self, 'RestApiDynamodb', partition_key='message')
        well_architected_stacks.simple_graphql_service.simple_graphql_service.SimpleGraphQlService(self, "SimpleGraphqlService")
        well_architected_stacks.waf_api_lambda_dynamodb.WafApiLambdaDynamodb(self, 'WafApiLambdaDynamodb')
        # saga_step_function.SagaStepFunction(self, "SagaStepFunction",)
        # event_bridge_atm.EventBridgeAtm(self, "EventBridgeAtm")
        # event_bridge_circuit_breaker.EventBridgeCircuitBreaker(
        #     self, 'EventBridgeCircuitBreaker',
        # )
        # event_bridge_etl.EventbridgeEtl(self, 'EventBridgeEtl', )

        # lambda_trilogy.lambda_lith.LambdaLith(self, "LambdaLith", )
        # lambda_trilogy.fat_lambda.TheFatLambdaStack(self, "FatLambda", )
        # lambda_trilogy.single_purpose_lambda.TheSinglePurposeFunctionStack(self, "SinglePurposeLambda", )
        # lambda_power_tuner.LambdaPowerTuner(self, "LambdaPowerTuner", )

    # def create_xray_tracer(self):
        # xray_tracer_sns_topic = sns_topic.SnsTopic(
        #     self, 'XRayTracerSnsFanOutTopic', display_name='The XRay Tracer Fan Out Topic'
        # ).topic
        # xray_tracer.sns_rest_api.SnsRestApi(
        #     self, 'SnsRestApi', sns_topic=xray_tracer_sns_topic
        # )
        # xray_tracer.sns_flow.SnsFlow(self, 'SnsFlow', sns_topic=xray_tracer_sns_topic)
        # xray_tracer.sqs_flow.SqsFlow(self, 'SqsFlow', sns_topic=xray_tracer_sns_topic)
        # xray_tracer.http_flow.HttpFlow(self, 'HttpFlow', sns_topic=xray_tracer_sns_topic)
        # xray_tracer.dynamodb_flow.DynamoDBFlow(
        #     self, 'DynamoDBFlow', sns_topic=xray_tracer_sns_topic
        # )

WellArchitected().synth()
