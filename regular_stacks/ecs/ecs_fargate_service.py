from enum import auto
import aws_cdk
import constructs

from . import autoscaling_ecs


class FargateService(autoscaling_ecs.AutoscalingEcsClusterConstruct):

    def __init__(self, scope: constructs.Construct, id: str,
        ecs_cluster=None,
        container_image=None,
        **kwargs
    ) -> None:
        super().__init__(
            scope, id,
            create_autoscaling_group_provider=False,
            **kwargs,
        )
        self.container_image = container_image
        self.ecs_cluster = ecs_cluster

    def create_alb_fargate_service(self):
        return aws_cdk.aws_ecs_patterns.ApplicationLoadBalancedFargateService(
            self, 'AlbEcsFargateService',
            assign_public_ip=True,
            cluster=self.ecs_cluster,
            task_image_options=aws_cdk.aws_ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=aws_cdk.aws_ecs.ContainerImage.from_registery(self.container_image)
            )
        )

    def create_nlb_fargate_service(self):
        return aws_cdk.aws_ecs_patterns.NetworkLoadBalancedFargateService(
            self, "NlbEcsFargateService",
            cluster= self.ecs_cluster,
            task_image_options=aws_cdk.aws_ecs_patterns.NetworkLoadBalancedTaskImageOptions(
                image=aws_cdk.aws_ecs.ContainerImage.from_registry(self.container_image)
            )
        )

    def add_security_group_ingress_rule(self, vpc_cidr_block=None, security_group=None):
        return security_group.add_ingress_rule(
            peer = aws_cdk.aws_ec2.Peer.ipv4(vpc_cidr_block),
            connection = aws_cdk.aws_ec2.Port.tcp(80),
            description="Allow http inbound from VPC"
        )