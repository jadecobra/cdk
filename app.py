import aws_cdk
import well_architected_stacks
import stacks.ecs.autoscaling_ecs_cluster
import stacks.ecs.nlb_autoscaling_ecs_service
import stacks.ecs.alb_autoscaling_ecs_service
import stacks.ecs.autoscaling_ecs_service
import stacks.ecs.autoscaling_ecs_service_with_placement
import stacks.ecs.nlb_fargate_service


class WellArchitected(aws_cdk.App):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_well_architected_stacks()
        self.lambda_trilogy()
        self.xray_tracer()
        self.ecs()

    def create_well_architected_stacks(self):
        well_architected_stacks.ApiLambdaDynamodbEventBridgeLambda(
            self, 'ApiLambdaDynamodbEventBridgeLambda',
        )
        well_architected_stacks.ApiLambdaDynamodbStack(
            self, 'ApiLambdaDynamodb',
            function_name='circuit_breaker_lambda',
            partition_key='id',
        )
        well_architected_stacks.ApiLambdaEventBridgeLambda(
            self, 'ApiLambdaEventBridgeLambda'
        )
        well_architected_stacks.ApiLambdaRds(self, 'ApiLambdaRds')
        well_architected_stacks.ApiLambdaSqsLambdaDynamodb(
            self, 'ApiLambdaSqsLambdaDynamodb'
        )
        well_architected_stacks.ApiStepFunctions(self, 'ApiStepFunctions')
        well_architected_stacks.LambdaPowerTuner(self, 'LambdaPowerTuner')
        well_architected_stacks.RestApiDynamodb(
            self, 'RestApiDynamodb',
            partition_key='message',
        )
        well_architected_stacks.RestApiSnsLambdaEventBridgeLambda(
            self, 'RestApiSnsLambdaEventBridgeLambda'
        )
        well_architected_stacks.RestApiSnsSqsLambda(self, 'RestApiSnsSqsLambda')
        well_architected_stacks.S3SqsLambdaEcsEventBridgeLambdaDynamodb(
            self, 'S3SqsLambdaEcsEventBridgeLambdaDynamodb'
        )
        well_architected_stacks.SagaStepFunction(self, 'SagaStepFunction')
        well_architected_stacks.SimpleGraphQlService(
            self, 'SimpleGraphqlService'
        )
        well_architected_stacks.WafApiLambdaDynamodb(
            self, 'WafApiLambdaDynamodb'
        )

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
        xray_tracer_sns_topic = well_architected_stacks.SnsTopic(
            self, 'XRayTracerSnsFanOutTopic',
            display_name='The XRay Tracer Fan Out Topic',
        )
        well_architected_stacks.RestApiSnsStack(
            self, 'RestApiSns',
            sns_topic=xray_tracer_sns_topic.sns_topic,
            error_topic=xray_tracer_sns_topic.error_topic,
        )
        well_architected_stacks.SnsLambdaSns(
            self, 'SnsLambdaSns',
            sns_topic=xray_tracer_sns_topic.sns_topic,
            error_topic=xray_tracer_sns_topic.error_topic,
        )
        well_architected_stacks.SqsLambdaSqs(
            self, 'SqsLambdaSqs',
            sns_topic=xray_tracer_sns_topic.sns_topic,
            error_topic=xray_tracer_sns_topic.error_topic,
        )
        well_architected_stacks.SnsLambda(
            self, 'SnsLambda',
            sns_topic=xray_tracer_sns_topic.sns_topic,
            error_topic=xray_tracer_sns_topic.error_topic,
        )
        well_architected_stacks.SnsLambdaDynamodb(
            self, 'SnsDynamodbLambda',
            sns_topic=xray_tracer_sns_topic.sns_topic,
            error_topic=xray_tracer_sns_topic.error_topic,
        )

    def ecs(self):
        def container_image():
            return "amazon/amazon-ecs-sample"

        stacks.ecs.autoscaling_ecs_cluster.AutoscalingEcsCluster(
            self, 'AutoscalingEcsCluster',
        )
        stacks.ecs.autoscaling_ecs_service.AutoscalingEcsService(
            self, 'AutoscalingEcsService',
            container_image='nginx:latest',
        )
        stacks.ecs.autoscaling_ecs_service_with_placement.AutoscalingEcsServiceWithPlacement(
            self, 'AutoscalingEcsServiceWithPlacement',
            container_image='nginx:latest',
        )
        stacks.ecs.alb_autoscaling_ecs_service.AlbAutoscalingEcsService(
            self, 'AlbAutoscalingEcsService',
            container_image=container_image(),
        )
        stacks.ecs.nlb_autoscaling_ecs_service.NlbAutoscalingEcsService(
            self, 'NlbAutoscalingEcsService',
            container_image=container_image(),
        )
        stacks.ecs.nlb_fargate_service.NlbFargateService(
            self, 'NlbFargateService',
            container_image=container_image(),
        )

WellArchitected().synth()

# TODO
# StateMachine examples - https://docs.amazon.com/step-functions/latest/dg/create-sample-projects.html
# EventBridge examples - https://docs.amazon.com/eventbridge/latest/userguide/eb-service-event.html
# Read Lambda Powertools docs