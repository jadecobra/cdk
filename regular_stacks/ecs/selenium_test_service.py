
import aws_cdk
import constructs
import well_architected_stacks


class SeleniumTestService(well_architected_stacks.well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, construct_id: str,
        name=None,
        max_capacity=None,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.name = name
        self.vpc = self.get_vpc()
        self.ecs_cluster = self.create_autoscaling_ecs_cluster()
        self.security_group = self.create_security_group()
        self.load_balancer = self.create_application_load_balancer(self.security_group)

        self.create_selenium_hub(
            max_capacity=max_capacity,
            security_group=self.security_group,
        )

        self.create_chrome_node(
            load_balancer_dns_name=self.load_balancer.load_balancer_dns_name,
            max_capacity=max_capacity,
            security_group=self.security_group,
        )
        self.create_firefox_node(
            load_balancer_dns_name=self.load_balancer.load_balancer_dns_name,
            max_capacity=max_capacity,
            security_group=self.security_group,
        )

        self.create_a_security_group_ingress_rule(
            connection=self.load_balancer.connections,
            port=self.default_port(),
        )

    def register_load_balancer_targets(self, service):
        return service.register_load_balancer_targets(
            aws_cdk.aws_ecs.EcsTarget(
                container_name='selenium-hub-container',
                container_port=self.default_port(),
                new_target_group_id='ECS',
                listener=aws_cdk.aws_ecs.ListenerConfig.application_listener(
                    listener=self.load_balancer.add_listener(
                        'Listener',
                        port=self.default_port(),
                        protocol=aws_cdk.aws_elasticloadbalancingv2.ApplicationProtocol.HTTP
                    ),
                    port=self.default_port(),
                    protocol=aws_cdk.aws_elasticloadbalancingv2.ApplicationProtocol.HTTPS
                )
            )
        )

    def create_security_group_ingress_rule(self, security_group=None, port=None):
        return security_group.add_ingress_rule(
            aws_cdk.aws_ec2.Peer.any_ipv4(),
            aws_cdk.aws_ec2.Port.tcp(port),
            f'Port {port} for inbound traffic'
        )

    def create_a_security_group_ingress_rule(self, connection=None, port=None):
        return connection.allow_from_any_ipv4(
            port_range=aws_cdk.aws_ec2.Port.tcp(port),
            description=f'Port {port} for inbound traffic'
        )

    def create_security_group(self):
        security_group = aws_cdk.aws_ec2.SecurityGroup(
            self, 'security-group-selenium',
            vpc=self.vpc,
            allow_all_outbound=True,
        )
        for port in (
            self.default_port(),
            self.entry_port(),
        ):
            self.create_security_group_ingress_rule(
                security_group=security_group,
                port=port,
            )
        return security_group

    @staticmethod
    def selenium_version():
        return '3.141.59'

    @staticmethod
    def entry_port():
        return 5555

    @staticmethod
    def default_port():
        return 4444

    def create_selenium_hub(self, max_capacity=None, security_group=None):
        service = self.create_autoscaling_fargate_service(
            name='selenium-hub',
            container_image=f'selenium/hub:{self.selenium_version()}',
            security_group=security_group,
            max_capacity=max_capacity,
            environment_variables={
                "GRID_BROWSER_TIMEOUT": "200000",
                "GRID_TIMEOUT": "180",
                "SE_OPTS": "-debug"
            }
        )
        self.register_load_balancer_targets(service)
        return service

    def create_chrome_node(self, load_balancer_dns_name=None, max_capacity=None, security_group=None):
        self.create_autoscaling_fargate_service(
            name='selenium-chrome-node',
            container_image=f'selenium/node-chrome:{self.selenium_version()}',
            max_capacity=max_capacity,
            security_group=security_group,
            environment_variables=self.get_node_environment_variables(load_balancer_dns_name),
            command=self.get_node_commands(),
            entry_point=self.get_entry_point_commands(),
        )

    def create_firefox_node(self, load_balancer_dns_name=None, max_capacity=None, security_group=None):
        self.create_autoscaling_fargate_service(
            name='selenium-firefox-node',
            container_image=f'selenium/node-firefox:{self.selenium_version()}',
            max_capacity=max_capacity,
            security_group=security_group,
            environment_variables=self.get_node_environment_variables(load_balancer_dns_name),
            command=self.get_node_commands(),
            entry_point=self.get_entry_point_commands(),
        )

    def create_scaling_configuration(self, service=None, max_capacity=None):
        service.auto_scale_task_count(
            min_capacity=1,
            max_capacity=max_capacity,
        ).scale_on_metric(
            "CpuScaling",
            metric=service.metric_cpu_utilization(
                period=self.sixty_seconds(),
                statistic='Maximum',
            ),
            evaluation_periods=1,
            scaling_steps=[
                aws_cdk.aws_applicationautoscaling.ScalingInterval(
                    change=-1,
                    upper=30
                ),
                aws_cdk.aws_applicationautoscaling.ScalingInterval(
                    change=3,
                    lower=80,
                ),
            ],
            adjustment_type=aws_cdk.aws_applicationautoscaling.AdjustmentType.CHANGE_IN_CAPACITY,
            cooldown=aws_cdk.Duration.seconds(180),
            metric_aggregation_type=aws_cdk.aws_applicationautoscaling.MetricAggregationType.MAXIMUM,
        )

    @staticmethod
    def get_entry_point_commands():
        return ["sh", "-c"]

    def get_node_commands(self):
        return [
            f"PRIVATE=$(curl -s http://169.254.170.2/v2/metadata | jq -r '.Containers[0].Networks[0].IPv4Addresses[0]') ; export REMOTE_HOST=\"http://$PRIVATE:{self.entry_port()}\"; export SE_OPTS=\"-host $PRIVATE -port {self.entry_port()}\" ; /opt/bin/entry_point.sh"
        ]

    def get_node_environment_variables(self, dns_name):
        return {
            f"HUB_PORT_{self.default_port()}_TCP_ADDR": dns_name,
            f"HUB_PORT_{self.default_port()}_TCP_PORT": f"{self.default_port()}",
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

    def create_autoscaling_group(self, security_group):
        return aws_cdk.aws_autoscaling.AutoScalingGroup(
            self, "AutoScalingGroup",
            instance_type=aws_cdk.aws_ec2.InstanceType("t2.micro"),
            machine_image=aws_cdk.aws_ecs.EcsOptimizedImage.amazon_linux2(),
            associate_public_ip_address=True,
            desired_capacity=5,
            vpc=self.vpc,
            vpc_subnets=self.get_subnets(),
            security_group=security_group,
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
                self.create_autoscaling_group(ecs_cluster.connections)
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

    @staticmethod
    def sixty_seconds():
        return aws_cdk.Duration.seconds(60)

    def create_application_load_balancer(self, security_group):
        load_balancer = aws_cdk.aws_elasticloadbalancingv2.ApplicationLoadBalancer(
            self, 'app-lb',
            idle_timeout=self.sixty_seconds(),
            vpc=self.vpc,
            deletion_protection=False,
            internet_facing=True,
        )
        load_balancer.add_security_group(security_group)
        return load_balancer

    def create_fargate_service(
        self, name=None, container_image=None,
        security_group=None, environment_variables=None,
        command=None, entry_point=None
    ):
        return aws_cdk.aws_ecs.FargateService(
            self, f'{name}FargateService',
            assign_public_ip=False,
            platform_version=aws_cdk.aws_ecs.FargatePlatformVersion.LATEST,
            cluster=self.ecs_cluster,
            capacity_provider_strategies=self.capacity_provider_strategies(),
            enable_execute_command=True,
            enable_ecs_managed_tags=False,
            max_healthy_percent=100,
            min_healthy_percent=75,
            service_name=name,
            security_groups=[security_group],
            task_definition=self.create_task_definition(
                container_image=container_image,
                port=self.default_port(),
                cpu=1024,
                name=name,
                memory=2048,
                environment=environment_variables,
                command=command,
                entry_point=entry_point,
            ),
        )

    def create_autoscaling_fargate_service(
        self, max_capacity=None, environment_variables=None, load_balancer=None, security_group=None,
        name=None, container_image=None, command=None, entry_point=None,
    ):
        service = self.create_fargate_service(
            name=name,
            container_image=container_image,
            security_group=security_group,
            environment_variables=environment_variables,
            command=command,
            entry_point=entry_point,
        )
        service.apply_removal_policy(aws_cdk.RemovalPolicy.DESTROY)
        self.create_scaling_configuration(
            service=service,
            max_capacity=max_capacity,
        )
        return service

    @staticmethod
    def runtime_platform():
        return aws_cdk.aws_ecs.RuntimePlatform(
            cpu_architecture=aws_cdk.aws_ecs.CpuArchitecture.ARM64,
        )