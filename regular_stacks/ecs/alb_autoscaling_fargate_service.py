import aws_cdk
import constructs
import well_architected_stacks

from . import alb_autoscaling_ecs_service


class AlbEcsFargateService(well_architected_stacks.well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        container_image=None,
        max_capacity=None,
        **kwargs
    ):
        super()._init__(scope, id, **kwargs)
        self.ecs_cluster = autoscaling_ecs.AutoscalingEcsClusterConstruct(
            self, 'AutoscalingEcs',
        ).ecs_cluster

        self.alb_fargate_service = self.create_fargate_service(
            cluster=self.ecs_cluster,
            container_image=container_image
        )

        self.alb_fargate_service.apply_removal_policy(aws_cdk.RemovalPolicy.DESTROY)

        scalabale_target = self.alb_fargate_service.auto_scale_task_count(
            min_capacity=1,
            max_capcaity=max_capacity
        )

        scalabale_target.scale_on_cpu_utilization(
            'CpuScaling',
            target_utilization_percent=50,
        )

        scalabale_target.scale_on_memory_utilization(
            'MemoryScaling',
            target_utilization_percent=50,
        )