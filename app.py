import aws_cdk

import well_architected_stacks.api_step_functions
import well_architected_stacks.circuit_breaker_lambda
import well_architected_stacks.event_bridge_atm
import well_architected_stacks.event_bridge_etl
import well_architected_stacks.rest_api_sns_sqs_lambda
import well_architected_stacks.rest_api_sns_lambda_eventbridge_lambda
import well_architected_stacks.rest_api_dynamodb
import well_architected_stacks.saga_step_function
import well_architected_stacks.simple_graphql_service.simple_graphql_service
import well_architected_stacks.waf_api_lambda_dynamodb
import well_architected_stacks.circuit_breaker_event_bridge
import well_architected_stacks.lambda_trilogy.lambda_fat
import well_architected_stacks.lambda_trilogy.lambda_lith
import well_architected_stacks.lambda_trilogy.lambda_single_purpose
import well_architected_stacks.lambda_trilogy.lambda_trilogy
import xray_tracer


class WellArchitected(aws_cdk.App):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        well_architected_stacks.api_step_functions.ApiStepFunctions(self, "ApiStepFunctions")
        well_architected_stacks.rest_api_sns_sqs_lambda.ApiSnsSqsLambda(self, 'ApiSnsSqsLambda')
        well_architected_stacks.rest_api_dynamodb.RestApiDynamodb(self, 'RestApiDynamodb', partition_key='message')
        well_architected_stacks.circuit_breaker_lambda.CircuitBreakerLambda(self, "CircuitBreakerLambda")
        well_architected_stacks.event_bridge_atm.EventBridgeAtm(self, "EventBridgeAtm")
        well_architected_stacks.event_bridge_etl.EventbridgeEtl(self, 'EventBridgeEtl')
        well_architected_stacks.rest_api_sns_lambda_eventbridge_lambda.ApiSnsLambdaEventBridgeLambda(self, "ApiSnsLambdaEventBridgeLambda")
        well_architected_stacks.saga_step_function.SagaStepFunction(self, "SagaStepFunction",)
        well_architected_stacks.simple_graphql_service.simple_graphql_service.SimpleGraphQlService(self, "SimpleGraphqlService")
        well_architected_stacks.waf_api_lambda_dynamodb.WafApiLambdaDynamodb(self, 'WafApiLambdaDynamodb')
        well_architected_stacks.circuit_breaker_event_bridge.CircuitBreakerEventBridge(
            self, 'CircuitBreakerEventBridge',
        )
        self.lambda_trilogy()
        self.xray_tracer()

        # lambda_power_tuner.LambdaPowerTuner(self, "LambdaPowerTuner", )

    def lambda_trilogy(self):
        # well_architected_stacks.lambda_trilogy.lambda_fat.LambdaFat(self, "LambdaFat", )
        well_architected_stacks.lambda_trilogy.lambda_lith.LambdaLith(self, "LambdaLith")
        # well_architected_stacks.lambda_trilogy.lambda_single_purpose.LambdaSinglePurpose(self, "LambdaSinglePurpose")
        well_architected_stacks.lambda_trilogy.lambda_trilogy.LambdaTrilogy(
            self, 'LambdaFat',
            function_name='lambda_fat',
        )
        well_architected_stacks.lambda_trilogy.lambda_trilogy.LambdaTrilogy(
            self, 'LambdaSinglePurpose',
            function_name='lambda_single_purpose',
        )

    def xray_tracer(self):
        xray_tracer_sns = xray_tracer.sns_topic.SnsTopic(
            self, 'XRayTracerSnsFanOutTopic',
            display_name='The XRay Tracer Fan Out Topic',
        )
        xray_tracer.sns_rest_api.SnsRestApi(
            self, 'SnsRestApi',
            sns_topic=xray_tracer_sns.sns_topic,
            error_topic=xray_tracer_sns.error_topic,
        )
        xray_tracer.sns_flow.SnsFlow(
            self, 'SnsFlow',
            sns_topic=xray_tracer_sns.sns_topic,
            error_topic=xray_tracer_sns.error_topic,
        )
        xray_tracer.sqs_flow.SqsFlow(
            self, 'SqsFlow',
            sns_topic=xray_tracer_sns.sns_topic,
            error_topic=xray_tracer_sns.error_topic,
        )
        xray_tracer.http_flow.HttpFlow(
            self, 'HttpFlow',
            sns_topic=xray_tracer_sns.sns_topic,
            error_topic=xray_tracer_sns.error_topic,
        )
        xray_tracer.dynamodb_flow.DynamoDBFlow(
            self, 'DynamoDBFlow',
            sns_topic=xray_tracer_sns.sns_topic,
            error_topic=xray_tracer_sns.error_topic,
        )

WellArchitected().synth()

# TODO
# StateMachine examples - https://docs.aws.amazon.com/step-functions/latest/dg/create-sample-projects.html