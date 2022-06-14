import aws_cdk
import well_architected_stacks
# import well_architected_stacks.api_step_functions
# import well_architected_stacks.circuit_breaker_lambda
# import well_architected_stacks.circuit_breaker_eventbridge
# import well_architected_stacks.eventbridge_atm
# import well_architected_stacks.eventbridge_etl
# import well_architected_stacks.lambda_trilogy.lambda_lith
# import well_architected_stacks.lambda_trilogy.lambda_trilogy
# import well_architected_stacks.rest_api_dynamodb
# import well_architected_stacks.rest_api_sns
# import well_architected_stacks.rest_api_sns_sqs_lambda
# import well_architected_stacks.rest_api_sns_lambda_eventbridge_lambda
# import well_architected_stacks.saga_step_function
# import well_architected_stacks.simple_graphql_service.simple_graphql_service
# import well_architected_stacks.sns_lambda_dynamodb
# import well_architected_stacks.sns_lambda
# import well_architected_stacks.sns_lambda_sns
# import well_architected_stacks.sns_topic
# import well_architected_stacks.sqs_lambda_sqs
# import well_architected_stacks.waf_api_lambda_dynamodb


class WellArchitected(aws_cdk.App):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        well_architected_stacks.api_step_functions.ApiStepFunctions(
            self, "ApiStepFunctions"
        )
        well_architected_stacks.rest_api_sns_sqs_lambda.ApiSnsSqsLambda(
            self, 'ApiSnsSqsLambda'
        )
        well_architected_stacks.rest_api_dynamodb.RestApiDynamodb(
            self, 'RestApiDynamodb',
            partition_key='message',
        )
        well_architected_stacks.circuit_breaker_lambda.CircuitBreakerLambda(
            self, "CircuitBreakerLambda"
        )
        well_architected_stacks.eventbridge_atm.EventBridgeAtm(
            self, "EventBridgeAtm"
        )
        well_architected_stacks.eventbridge_etl.EventbridgeEtl(
            self, 'EventBridgeEtl'
        )
        well_architected_stacks.rest_api_sns_lambda_eventbridge_lambda.ApiSnsLambdaEventBridgeLambda(
            self, "ApiSnsLambdaEventBridgeLambda"
        )
        well_architected_stacks.saga_step_function.SagaStepFunction(
            self, "SagaStepFunction",
        )
        well_architected_stacks.simple_graphql_service.SimpleGraphQlService(
        # well_architected_stacks.simple_graphql_service.simple_graphql_service.SimpleGraphQlService(
            self, "SimpleGraphqlService"
        )
        well_architected_stacks.waf_api_lambda_dynamodb.WafApiLambdaDynamodb(
            self, 'WafApiLambdaDynamodb'
        )
        well_architected_stacks.circuit_breaker_eventbridge.CircuitBreakerEventBridge(
            self, 'CircuitBreakerEventBridge',
        )
        self.lambda_trilogy()
        self.xray_tracer()

        # lambda_power_tuner.LambdaPowerTuner(self, "LambdaPowerTuner", )

    def lambda_trilogy(self):
        well_architected_stacks.lambda_trilogy.LambdaLith(self, "LambdaLith")
        well_architected_stacks.lambda_trilogy.LambdaTrilogy(
            self, 'LambdaFat',
            function_name='lambda_fat',
        )
        well_architected_stacks.lambda_trilogy.LambdaTrilogy(
            self, 'LambdaSinglePurpose',
            function_name='lambda_single_purpose',
        )

    def xray_tracer(self):
        xray_tracer_sns_topic = well_architected_stacks.sns_topic.SnsTopic(
            self, 'XRayTracerSnsFanOutTopic',
            display_name='The XRay Tracer Fan Out Topic',
        )
        well_architected_stacks.rest_api_sns.RestApiSnsStack(
            self, 'RestApiSns',
            sns_topic=xray_tracer_sns_topic.sns_topic,
            error_topic=xray_tracer_sns_topic.error_topic,
        )
        well_architected_stacks.sns_lambda_sns.SnsLambdaSns(
            self, 'SnsLambdaSns',
            sns_topic=xray_tracer_sns_topic.sns_topic,
            error_topic=xray_tracer_sns_topic.error_topic,
        )
        well_architected_stacks.sqs_lambda_sqs.SqsLambdaSqs(
            self, 'SqsLambdaSqs',
            sns_topic=xray_tracer_sns_topic.sns_topic,
            error_topic=xray_tracer_sns_topic.error_topic,
        )
        well_architected_stacks.sns_lambda.SnsLambda(
            self, 'SnsLambda',
            sns_topic=xray_tracer_sns_topic.sns_topic,
            error_topic=xray_tracer_sns_topic.error_topic,
        )
        well_architected_stacks.sns_lambda_dynamodb.SnsLambdaDynamodb(
            self, 'SnsDynamodbLambda',
            sns_topic=xray_tracer_sns_topic.sns_topic,
            error_topic=xray_tracer_sns_topic.error_topic,
        )

WellArchitected().synth()

# TODO
# StateMachine examples - https://docs.aws.amazon.com/step-functions/latest/dg/create-sample-projects.html
# EventBridge examples - https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-service-event.html
# Read Lambda Powertools docs