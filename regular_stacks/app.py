import aws_cdk
import ecs
import batch


class RegularStacks(aws_cdk.App):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ecs()
        self.selenium()
        self.regular_stacks()

    @staticmethod
    def container_image():
        return "amazon/amazon-ecs-sample"

    def ecs(self):
        ecs.autoscaling_ecs_cluster.AutoscalingEcsCluster(
            self, 'AutoscalingEcsCluster',
        )
        ecs.autoscaling_ecs_service.AutoscalingEcsService(
            self, 'AutoscalingEcsService',
            container_image='nginx:latest',
        )
        ecs.autoscaling_ecs_service_with_placement.AutoscalingEcsServiceWithPlacement(
            self, 'AutoscalingEcsServiceWithPlacement',
            container_image='nginx:latest',
        )
        ecs.alb_autoscaling_ecs_service.AlbAutoscalingEcsService(
            self, 'AlbAutoscalingEcsService',
            container_image=self.container_image(),
        )
        ecs.nlb_autoscaling_ecs_service.NlbAutoscalingEcsService(
            self, 'NlbAutoscalingEcsService',
            container_image=self.container_image(),
        )
        ecs.nlb_fargate_service.NlbFargateService(
            self, 'NlbFargateService',
            container_image=self.container_image(),
        )
        ecs.alb_fargate_service.AlbFargateService(
            self, 'AlbFargateService',
            container_image=self.container_image(),
        )
        ecs.nlb_autoscaling_fargate_service.NlbAutoscalingFargateService(
            self, 'NlbAutoscalingFargateService',
            container_image=self.container_image(),
        )

        # ecs.nlb_ec2_service.NlbEc2Service(
        #     self, 'NlbEc2Service',
        #     container_image=self.container_image(),
        # )
        # ecs.alb_ec2_service.AlbEc2Service(
        #     self, 'AlbEc2Service',
        #     container_image=self.container_image(),
        # )

    def selenium(self):
        ecs.selenium_test_service.SeleniumTestService(
            self, 'SeleniumTestService',
            cpu=1024,
            max_capacity=10,
            memory=2048,
        )

    def regular_stacks(self):
        batch.BatchEC2Stack(
            self, 'BatchEC2Stack',
            container_name='public.ecr.aws/amazonlinux/amazonlinux:latest',
            number_of_environments=3,
        )

RegularStacks().synth()

# TODO
# StateMachine examples - https://docs.aws.amazon.com/step-functions/latest/dg/create-sample-projects.html
# Read Lambda Powertools docs
# Add EventPattern as LambdaFunction input