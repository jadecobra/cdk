
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

        self.ecs_cluster.add_asg_capacity_provider(
            self.create_autoscaling_capacity_provider(
                self.create_autoscaling_group()
            )
        )

    @staticmethod
    def create_capacity_provider_strategies(self):
        return [
            aws_cdk.aws_ecs.CapacityProviderStrategy(
                capacity_provider='FARGATE',
                weight=1,
                base=4,
            ),
            aws_cdk.aws_ecs.CapacityProviderStrategy(
                capacity_provider='FARGATE_SPOT',
                weight=4
            )
        ]

    def get_subnets(self):
        return aws_cdk.aws_ec2.SubnetSelection(
            subnet_type=aws_cdk.aws_ec2.SubnetType.PUBLIC
        )

    def create_autoscaling_group(self):
        return aws_cdk.aws_autoscaling.AutoScalingGroup(
            self, "AutoScalingGroup",
            instance_type=aws_cdk.aws_ec2.InstanceType("t2.micro"),
            machine_image=aws_cdk.aws_ecs.EcsOptimizedImage.amazon_linux2(),
            associate_public_ip_address=True,
            desired_capacity=5,
            vpc=self.vpc,
            vpc_subnets=self.get_subnets(),
        )

    def create_autoscaling_capacity_provider(self, autoscaling_group):
        return aws_cdk.aws_ecs.AsgCapacityProvider(
            self, "AsgCapacityProvider",
            auto_scaling_group=autoscaling_group,
            spot_instance_draining=True,
            machine_image_type=aws_cdk.aws_ecs.MachineImageType.AMAZON_LINUX_2,
        )

    def create_ecs_cluster(self):
        return aws_cdk.aws_ecs.Cluster(
            self, 'SeleniumHubCluster',
            enable_fargate_capacity_providers=False,
            container_insights=True,
            vpc=self.vpc
        )

    def create_fargate_service(self, cluster=None, container_image=None):
        return aws_cdk.aws_ecs_patterns.ApplicationLoadBalancedFargateService(
            self, 'AlbEcsFargateService',
            assign_public_ip=False,
            capacity_provider_strategies=[
                aws_cdk.aws_ecs.CapacityProviderStrategy(
                    capacity_provider='FARGATE',
                    weight=1,
                    base=4,
                ),
                aws_cdk.aws_ecs.CapacityProviderStrategy(
                    capacity_provider='FARGATE_SPOT',
                    weight=4
                )
            ],
            max_healthy_percent=100,
            min_healthy_percent=75,
            listener_port=4444,
            target_protocol=aws_cdk.aws_elasticloadbalancingv2.ApplicationProtocol.HTTPS,
            cluster=cluster,
            task_image_options=aws_cdk.aws_ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=aws_cdk.aws_ecs.ContainerImage.from_registry(
                    container_image
                )
            ),
        )
