import aws_cdk
import well_architected.stacks
import well_architected.stacks.api_lambda_dynamodb_event_bridge_lambda
import well_architected.stacks.api_lambda_dynamodb
# import regular_stacks.ecs

class WellArchitected(aws_cdk.App):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_well_architected_stacks()
        # self.lambda_trilogy()
        # self.xray_tracer()
        # self.ecs()
        # self.in_progress()

    def create_well_architected_stacks(self):
        well_architected.stacks.api_lambda_dynamodb_event_bridge_lambda.ApiLambdaDynamodbEventBridgeLambda(
            self, 'ApiLambdaDynamodbEventBridgeLambda',
        )
        # well_architected.stacks.api_lambda_dynamodb.ApiLambdaDynamodbStack(
        #     self, 'ApiLambdaDynamodb',
        #     function_name='circuit_breaker_lambda',
        #     partition_key='id',
        # )
        # well_architected.stacks.api_lambda_eventbridge_lambda.ApiLambdaEventBridgeLambda(
        #     self, 'ApiLambdaEventBridgeLambda'
        # )
        # well_architected.stacks.api_lambda_rds.ApiLambdaRds(self, 'ApiLambdaRds')
        # well_architected.stacks.api_lambda_sqs_lambda_dynamodb.ApiLambdaSqsLambdaDynamodb(
        #     self, 'ApiLambdaSqsLambdaDynamodb'
        # )
        # well_architected.stacks.api_stepfunctions.ApiStepFunctions(self, 'ApiStepFunctions')
        # well_architected.stacks.lambda_power_tuner.LambdaPowerTuner(self, 'LambdaPowerTuner')
        # well_architected.stacks.rest_api_dynamodb.RestApiDynamodb(
        #     self, 'RestApiDynamodb',
        #     partition_key='message',
        # )
        # well_architected.stacks.rest_api_sns_lambda_eventbridge_lambda.RestApiSnsLambdaEventBridgeLambda(
        #     self, 'RestApiSnsLambdaEventBridgeLambda'
        # )
        # well_architected.stacks.RestApiSnsSqsLambda(self, 'RestApiSnsSqsLambda')
        # well_architected.stacks.S3SqsLambdaEcsEventBridgeLambdaDynamodb(
        #     self, 'S3SqsLambdaEcsEventBridgeLambdaDynamodb'
        # )
        # well_architected.stacks.SagaStepFunction(self, 'SagaStepFunction')
        # well_architected.stacks.SimpleGraphQlService(
        #     self, 'SimpleGraphqlService'
        # )
        # well_architected.stacks.WafApiLambdaDynamodb(
        #     self, 'WafApiLambdaDynamodb'
        # )

    def lambda_trilogy(self):
        well_architected.stacks.lambda_trilogy.LambdaLith(self, "LambdaLith")
        well_architected.stacks.lambda_trilogy.LambdaTrilogy(
            self, 'LambdaFat',
            function_name='lambda_fat',
        )
        well_architected.stacks.lambda_trilogy.LambdaTrilogy(
            self, 'LambdaSinglePurpose',
            function_name='lambda_single_purpose',
        )

    def xray_tracer(self):
        xray_tracer_sns_topic = well_architected.stacks.SnsTopic(
            self, 'XRayTracerSnsFanOutTopic',
            display_name='The XRay Tracer Fan Out Topic',
        )
        well_architected.stacks.RestApiSnsStack(
            self, 'RestApiSns',
            sns_topic=xray_tracer_sns_topic.sns_topic,
            error_topic=xray_tracer_sns_topic.error_topic,
        )
        well_architected.stacks.SnsLambdaSns(
            self, 'SnsLambdaSns',
            sns_topic=xray_tracer_sns_topic.sns_topic,
            error_topic=xray_tracer_sns_topic.error_topic,
        )
        well_architected.stacks.SqsLambdaSqs(
            self, 'SqsLambdaSqs',
            sns_topic=xray_tracer_sns_topic.sns_topic,
            error_topic=xray_tracer_sns_topic.error_topic,
        )
        well_architected.stacks.SnsLambda(
            self, 'SnsLambda',
            sns_topic=xray_tracer_sns_topic.sns_topic,
            error_topic=xray_tracer_sns_topic.error_topic,
        )
        well_architected.stacks.SnsLambdaDynamodb(
            self, 'SnsDynamodbLambda',
            sns_topic=xray_tracer_sns_topic.sns_topic,
            error_topic=xray_tracer_sns_topic.error_topic,
        )

    # def ecs(self):
    #     def container_image():
    #         return "amazon/amazon-ecs-sample"

    #     stacks.ecs.autoscaling_ecs_cluster.AutoscalingEcsCluster(
    #         self, 'AutoscalingEcsCluster',
    #     )
    #     stacks.ecs.autoscaling_ecs_service.AutoscalingEcsService(
    #         self, 'AutoscalingEcsService',
    #         container_image='nginx:latest',
    #     )
    #     stacks.ecs.autoscaling_ecs_service_with_placement.AutoscalingEcsServiceWithPlacement(
    #         self, 'AutoscalingEcsServiceWithPlacement',
    #         container_image='nginx:latest',
    #     )
    #     stacks.ecs.alb_autoscaling_ecs_service.AlbAutoscalingEcsService(
    #         self, 'AlbAutoscalingEcsService',
    #         container_image=container_image(),
    #     )
    #     stacks.ecs.nlb_autoscaling_ecs_service.NlbAutoscalingEcsService(
    #         self, 'NlbAutoscalingEcsService',
    #         container_image=container_image(),
    #     )
    #     stacks.ecs.nlb_fargate_service.NlbFargateService(
    #         self, 'NlbFargateService',
    #         container_image=container_image(),
    #     )
    #     stacks.ecs.nlb_autoscaling_fargate_service.NlbAutoscalingFargateService(
    #         self, 'NlbAutoscalingFargateService',
    #         container_image=container_image()
    #     )

WellArchitected().synth()

# TODO
# StateMachine examples - https://docs.aws.amazon.com/step-functions/latest/dg/create-sample-projects.html
# Read Lambda Powertools docs