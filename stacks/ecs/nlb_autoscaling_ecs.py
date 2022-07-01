import aws_cdk
import constructs
import regular_constructs.autoscaling_ecs_cluster
import well_architected


class NlbAutoscalingEcs(well_architected.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        container_image=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, *kwargs)

        ecs_cluster = regular_constructs.autoscaling_ecs_cluster.AutoscalingEcsClusterConstruct(
            self, 'AutoscalingEcs',
        )
        ecs_cluster.create_autoscaling_group_provider(
            self.create_autoscaling_group(ecs_cluster.vpc)
        )

        ecs_service = self.create_ecs_service(
            ecs_cluster=ecs_cluster.ecs_cluster,
            task_image_options=self.get_task_image_options(container_image)
        )

        aws_cdk.CfnOutput(
            self, "LoadBalancerDNS",
            value=ecs_service.load_balancer.load_balancer_dns_name
        )

    def create_autoscaling_group(self, vpc):
        return aws_cdk.aws_autoscaling.AutoScalingGroup(
            self, "AutoScalingGroup",
            instance_type=aws_cdk.aws_ec2.InstanceType("t2.micro"),
            machine_image=aws_cdk.aws_ecs.EcsOptimizedImage.amazon_linux2(),
            vpc=vpc,
        )

    def get_task_image_options(self, container_image):
        return aws_cdk.aws_ecs_patterns.NetworkLoadBalancedTaskImageOptions(
            image=aws_cdk.aws_ecs.ContainerImage.from_registry(
                container_image
            )
        )

    def create_ecs_service(self, ecs_cluster=None, task_image_options=None):
        return aws_cdk.aws_ecs_patterns.NetworkLoadBalancedEc2Service(
            self, "Ec2Service",
            cluster=ecs_cluster,
            memory_limit_mib=512,
            task_image_options=task_image_options,
        )
