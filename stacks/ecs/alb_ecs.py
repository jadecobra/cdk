import aws_cdk
import constructs
import regular_constructs.autoscaling_ecs

class AlbEcs(aws_cdk.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        ecs_cluster = regular_constructs.autoscaling_ecs.AutoscalingEcsConstruct(
            self, 'AutoscalingEcs',
        )
        ecs_cluster.create_autoscaling_group_provider(
            self.create_autoscaling_group(ecs_cluster.vpc)
        )

        ecs_task_definition = self.create_task_definition()

        self.create_container(
            task_definition=ecs_task_definition,
            image_name="amazon/amazon-ecs-sample"
        )

        service = aws_cdk.aws_ecs.Ec2Service(
            self, "Service",
            cluster=ecs_cluster.ecs_cluster,
            task_definition=ecs_task_definition
        )

        application_load_balancer = self.create_application_load_balancer(
            vpc=ecs_cluster.vpc,
            service=service
        )

        aws_cdk.CfnOutput(
            self, "LoadBalancerDNS",
            value=application_load_balancer.load_balancer_dns_name
        )

    @staticmethod
    def container_port():
        return 80

    def create_application_load_balancer(self, vpc=None, service=None):
        application_load_balancer = aws_cdk.aws_elasticloadbalancingv2.ApplicationLoadBalancer(
            self, "ApplicationLoadBalancer",
            vpc=vpc,
            internet_facing=True
        )
        application_load_balancer.add_listener(
            "PublicListener",
            port=self.container_port(),
            open=True
        ).add_targets(
            "Targets",
            port=self.container_port(),
            targets=[service],
            health_check=self.create_health_check(),
        )
        return application_load_balancer

    @staticmethod
    def create_health_check():
        return aws_cdk.aws_elasticloadbalancingv2.HealthCheck(
            interval=aws_cdk.Duration.seconds(60),
            path="/health",
            timeout=aws_cdk.Duration.seconds(5)
        )

    def create_task_definition(self):
        return aws_cdk.aws_ecs.Ec2TaskDefinition(
            self, "TaskDefinition"
        )

    def get_port_mappings(self):
        return aws_cdk.aws_ecs.PortMapping(
            container_port=self.container_port(),
            host_port=8080,
            protocol=aws_cdk.aws_ecs.Protocol.TCP
        )

    def create_container(self, task_definition=None, image_name=None):
        container = task_definition.add_container(
            "Container",
            image=aws_cdk.aws_ecs.ContainerImage.from_registry(image_name),
            memory_limit_mib=256
        )
        container.add_port_mappings(
            self.get_port_mappings()
        )
        return container

    def create_autoscaling_group(self, vpc):
        return aws_cdk.aws_autoscaling.AutoScalingGroup(
            self, "AutoScalingGroup",
            instance_type=aws_cdk.aws_ec2.InstanceType.of(
                aws_cdk.aws_ec2.InstanceClass.BURSTABLE3,
                aws_cdk.aws_ec2.InstanceSize.MICRO
            ),
            machine_image=aws_cdk.aws_ecs.EcsOptimizedImage.amazon_linux2(),
            vpc=vpc,
        )