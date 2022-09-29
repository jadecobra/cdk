
import aws_cdk
import constructs
import well_architected_stacks


class SeleniumTestService(well_architected_stacks.well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, construct_id: str,
        container_image=None,
        max_capacity=None,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.vpc = self.get_vpc()
        self.ecs_cluster = self.create_ecs_cluster()

        self.alb_fargate_service = self.create_fargate_service(
            cluster=self.ecs_cluster,
            container_image=container_image,
        )
        self.alb_fargate_service.service.apply_removal_policy(
            aws_cdk.RemovalPolicy.DESTROY
        )
        scalable_task = self.alb_fargate_service.service.auto_scale_task_count(
            min_capacity=1,
            max_capacity=max_capacity
        )

        scalable_task.scale_on_cpu_utilization(
            "CpuScaling",
            target_utilization_percent=70
        )

    def create_ecs_cluster(self):
        return aws_cdk.aws_ecs.Cluster(
            self, 'SeleniumHubCluster',
            vpc=self.vpc
        )

    def create_fargate_service(self, cluster=None, container_image=None):
        return aws_cdk.aws_ecs_patterns.ApplicationLoadBalancedFargateService(
            self, 'AlbEcsFargateService',
            assign_public_ip=False,
            max_healthy_percent=100,
            min_healthy_percent=75,
            listener_port=4444,
            cluster=cluster,
            task_image_options=aws_cdk.aws_ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=aws_cdk.aws_ecs.ContainerImage.from_registry(
                    container_image
                )
            ),
        )
