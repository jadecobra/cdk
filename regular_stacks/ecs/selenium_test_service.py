
import aws_cdk
import constructs
import well_architected_stacks


class SeleniumTestService(well_architected_stacks.well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, construct_id: str,
        name=None,
        container_image=None,
        max_capacity=None,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.name = name
        self.vpc = self.get_vpc()
        self.ecs_cluster = self.create_autoscaling_ecs_cluster()
        # self.ecs_cluster.connections.allow_from_any_ipv4(
        #     port_range=aws_cdk.aws_ec2.Port.tcp(4444),
        #     description="Port 5555 for inbound traffic",

        # )
        self.ecs_cluster.connections.allow_from_any_ipv4(
            port_range=aws_cdk.aws_ec2.Port.tcp(5555),
            description="Port 5555 for inbound traffic",
        )
        # self.create_selenium_hub()
        # self.create_chrome_node()
        # self.create_firefox_node()

        self.selenium_hub = self.create_fargate_service(
            name='selenium-hub',
            container_image='selenium/hub:3.141.59',
            port=4444,
            environment={
                "GRID_BROWSER_TIMEOUT": "200000",
                "GRID_TIMEOUT": "180",
                "SE_OPTS": "-debug"
            }
        )
        self.chrome_hub = self.create_fargate_service(
            name='selenium-chrome-node',
            container_image='selenium/node-chrome:3.141.59',
            port=4444,
            environment=self.get_node_environment_variables(),
            command=self.get_node_commands(),
            entry_point=self.get_entry_point_commands(),
        )

        self.firefox_hub = self.create_fargate_service(
            name='selenium-firefox-node',
            container_image='selenium/node-firefox:3.141.59',
            port=4444,
            environment=self.get_node_environment_variables(),
            command=self.get_node_commands(),
            entry_point=self.get_entry_point_commands(),
        )
        self.selenium_hub.apply_removal_policy(
            aws_cdk.RemovalPolicy.DESTROY
        )
        scalable_task = self.selenium_hub.auto_scale_task_count(
            min_capacity=1,
            max_capacity=max_capacity
        )

        scalable_task.scale_on_cpu_utilization(
            "CpuScaling",
            target_utilization_percent=70
        )

    @staticmethod
    def get_entry_point_commands():
        return ["sh", "-c"]

    @staticmethod
    def get_node_commands():
        return [
            "PRIVATE=$(curl -s http://169.254.170.2/v2/metadata | jq -r '.Containers[0].Networks[0].IPv4Addresses[0]') ; export REMOTE_HOST=\"http://$PRIVATE:5555\"; export SE_OPTS=\"-host $PRIVATE -port 5555\" ; /opt/bin/entry_point.sh"
        ]

    def get_node_environment_variables(self):
        return {
            "HUB_PORT_4444_TCP_ADDR": self.selenium_hub.load_balancer.load_balancer_dns_name,
            "HUB_PORT_4444_TCP_PORT": "4444",
            "NODE_MAX_INSTANCES": "500",
            "NODE_MAX_SESSION": "500",
            "SE_OPTS": "-debug",
            "shm_size": "512",
        }

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

    @staticmethod
    def create_log_driver(name):
        return aws_cdk.aws_ecs.LogDriver.aws_logs(
            stream_prefix=f'{name}-logs'
        )

    def create_task_definition(
        self, name=None, container_image=None, port=None, cpu=None, memory=None,
        environment=None, command=None, entry_point=None,
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
            command=command,
            container_name=f'{name}-container',
            cpu=cpu,
            entry_point=entry_point,
            environment=environment,
            essential=True,
            image=aws_cdk.aws_ecs.ContainerImage.from_registry(container_image),
            memory_limit_mib=memory,
            port_mappings=self.get_port_mappings(port),
            logging=self.create_log_driver(name)
        )
        return task_definition

    def create_application_load_balancer(self):
        return

    def create_fargate_service(
        self, name=None, container_image=None, port=None,
        environment=None, command=None, entry_point=None
    ):
        return aws_cdk.aws_ecs.FargateService(
            self, f'{name}FargateService',
            assign_public_ip=False,
            platform_version=aws_cdk.aws_ecs.FargatePlatformVersion.LATEST,
            cluster=self.ecs_cluster,
            capacity_provider_strategies=self.capacity_provider_strategies(),
            enable_execute_command=True,
            enable_ecs_managed_tags=False,
            health_check_grace_period=aws_cdk.Duration.seconds(60),
            max_healthy_percent=100,
            min_healthy_percent=75,
            service_name=name,
            task_definition=self.create_task_definition(
                container_image=container_image,
                port=port,
                cpu=1024,
                name=name,
                memory=2048,
                environment=environment,
                command=command,
                entry_point=entry_point,
            ),
        )

    # def create_fargate_service(self, name=None, container_image=None, environment=None, port=None, command=None, entry_point=None):
    #     return aws_cdk.aws_ecs_patterns.ApplicationLoadBalancedFargateService(
    #         self, f'{name}AlbEcsFargateService',
    #         assign_public_ip=False,
    #         capacity_provider_strategies=self.capacity_provider_strategies(),
    #         enable_execute_command=True,
    #         max_healthy_percent=100,
    #         min_healthy_percent=75,
    #         listener_port=port,
    #         open_listener=False,
    #         cluster=self.ecs_cluster,
    #         runtime_platform=aws_cdk.aws_ecs.RuntimePlatform(
    #             cpu_architecture=aws_cdk.aws_ecs.CpuArchitecture.ARM64,
    #         ),
    #         task_definition=self.create_task_definition(
    #             container_image=container_image,
    #             port=port,
    #             cpu=1024,
    #             name=name,
    #             memory=2048,
    #             environment=environment,
    #             command=command,
    #             entry_point=entry_point,
    #         ),
    #     )
