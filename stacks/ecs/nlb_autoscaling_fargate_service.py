import aws_cdk
import constructs
import regular_constructs.autoscaling_ecs
import well_architected

from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    App, CfnOutput, Duration, Stack
)
from constructs import Construct


class NlbAutoscalingFargateService(well_architected.Stack):

    def __init__(self, scope: Construct, id: str,
        container_image=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        autoscaling_ecs_cluster = regular_constructs.autoscaling_ecs.AutoscalingEcsCluster(
            self, 'EcsCluster',
            create_autoscaling_group_provider=False
        )

        fargate_service = ecs_patterns.NetworkLoadBalancedFargateService(
            self, "sample-app",
            cluster=autoscaling_ecs_cluster.ecs_cluster,
            task_image_options=ecs_patterns.NetworkLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry(container_image)
            )
        )

        fargate_service.service.connections.security_groups[0].add_ingress_rule(
            peer = ec2.Peer.ipv4(autoscaling_ecs_cluster.vpc.vpc_cidr_block),
            connection = ec2.Port.tcp(80),
            description="Allow http inbound from VPC"
        )

        # Setup AutoScaling policy
        scaling = fargate_service.service.auto_scale_task_count(
            max_capacity=2
        )
        scaling.scale_on_cpu_utilization(
            "CpuScaling",
            target_utilization_percent=50,
            scale_in_cooldown=Duration.seconds(60),
            scale_out_cooldown=Duration.seconds(60),
        )

        CfnOutput(
            self, "LoadBalancerDNS",
            value=fargate_service.load_balancer.load_balancer_dns_name
        )
