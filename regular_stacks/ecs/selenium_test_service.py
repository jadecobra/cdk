
import aws_cdk
import constructs
import well_architected_stacks


class SeleniumTestService(well_architected_stacks.well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, construct_id: str,
        name=None,
        container_image=None,
        container_name=None,
        max_capacity=None,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.name = name
        self.vpc = self.get_vpc()
        self.ecs_cluster = self.create_autoscaling_ecs_cluster()
        # self.create_selenium_hub()
        # self.create_chrome_node()
        # self.create_firefox_node()

        self.selenium_hub = self.create_fargate_service(
            container_image=container_image,
            container_name=f'{self.name}-container',
            port=4444,
            environment={
                "GRID_BROWSER_TIMEOUT": "200000",
                "GRID_TIMEOUT": "180",
                "SE_OPTS": "-debug"
            }
        )
        self.selenium_hub.service.apply_removal_policy(
            aws_cdk.RemovalPolicy.DESTROY
        )
        scalable_task = self.selenium_hub.service.auto_scale_task_count(
            min_capacity=1,
            max_capacity=max_capacity
        )

        scalable_task.scale_on_cpu_utilization(
            "CpuScaling",
            target_utilization_percent=70
        )



    @staticmethod
    def capacity_provider_strategies():
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

    def create_autoscaling_ecs_cluster(self):
        ecs_cluster = aws_cdk.aws_ecs.Cluster(
            self, 'SeleniumHubCluster',
            enable_fargate_capacity_providers=False,
            container_insights=True,
            vpc=self.vpc
        )
        ecs_cluster.add_asg_capacity_provider(
            self.create_autoscaling_capacity_provider(
                self.create_autoscaling_group()
            )
        )
        return ecs_cluster

    @staticmethod
    def get_port_mappings(port):
        return [
            aws_cdk.aws_ecs.PortMapping(
                container_port=port,
                host_port=port,
            )
        ]

    def create_task_definition(
        self, name=None, container_image=None, container_name=None,
        port=None, cpu=None, memory=None,
        environment=None,
    ):
        task_definition = aws_cdk.aws_ecs.FargateTaskDefinition(
            self, f'{name}FargateTaskDefinition',
            cpu=cpu,
            memory_limit_mib=memory,
            runtime_platform=aws_cdk.aws_ecs.RuntimePlatform(
                cpu_architecture=aws_cdk.aws_ecs.CpuArchitecture.ARM64,
            ),
        )
        task_definition.add_container(
            f'{name}Container',
            image=aws_cdk.aws_ecs.ContainerImage.from_registry(container_image),
            cpu=cpu,
            memory_limit_mib=memory,
            container_name=container_name,
            essential=True,
            environment=environment,
            port_mappings=self.get_port_mappings(port),
            logging=aws_cdk.aws_ecs.LogDriver.aws_logs(
                stream_prefix=f'{name}-logs'
            )
        )
        return task_definition

    def create_fargate_service(self, name=None, container_image=None, container_name=None, environment=None, port=None):
        return aws_cdk.aws_ecs_patterns.ApplicationLoadBalancedFargateService(
            self, f'{name}AlbEcsFargateService',
            assign_public_ip=False,
            capacity_provider_strategies=self.capacity_provider_strategies(),
            enable_execute_command=True,
            max_healthy_percent=100,
            min_healthy_percent=75,
            listener_port=port,
            open_listener=False,
            cluster=self.ecs_cluster,
            runtime_platform=aws_cdk.aws_ecs.RuntimePlatform(
                cpu_architecture=aws_cdk.aws_ecs.CpuArchitecture.ARM64,
            ),
            task_definition=self.create_task_definition(
                container_image=container_image,
                container_name=container_name,
                port=port,
                cpu=1024,
                name=self.name,
                memory=2048,
                environment=environment,
            ),
        )
