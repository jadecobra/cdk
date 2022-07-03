from venv import create
import aws_cdk
import constructs
import regular_constructs.autoscaling_ecs
import well_architected


class NlbFargateService(well_architected.Stack):

    def __init__(self, scope: constructs.Construct, id: str,
        container_image=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        autoscaling_ecs_cluster = regular_constructs.autoscaling_ecs.AutoscalingEcsCluster(
            self, 'AutoscalingEcsCluster',
            create_autoscaling_group_provider=False,
        )

        fargate_service = self.create_fargate_service(
            ecs_cluster=autoscaling_ecs_cluster.ecs_cluster,
            container_image=container_image,
        )

        fargate_service.service.connections.security_groups[0].add_ingress_rule(
            peer=aws_cdk.aws_ec2.Peer.ipv4(autoscaling_ecs_cluster.vpc.vpc_cidr_block),
            connection=aws_cdk.aws_ec2.Port.tcp(80),
            description="Allow http inbound from VPC"
        )

        aws_cdk.CfnOutput(
            self, "LoadBalancerDNS",
            value=fargate_service.load_balancer.load_balancer_dns_name
        )

    def create_fargate_service(self, ecs_cluster=None, container_image=None):
        return aws_cdk.aws_ecs_patterns.NetworkLoadBalancedFargateService(
            self, "FargateService",
            cluster=ecs_cluster,
            task_image_options=aws_cdk.aws_ecs_patterns.NetworkLoadBalancedTaskImageOptions(
                image=aws_cdk.aws_ecs.ContainerImage.from_registry(container_image)
            )
        )