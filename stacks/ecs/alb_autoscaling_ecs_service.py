import aws_cdk
import constructs
import well_architected
import regular_constructs.autoscaling_ecs


class AlbAutoscalingEcsService(well_architected.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        container_image=None,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        ecs_cluster = self.create_ecs_cluster()
        ecs_cluster.create_container(
            container_image=container_image
        )

        aws_cdk.CfnOutput(
            self, "LoadBalancerDNS",
            value=self.get_application_load_balancer_dns_name(
                vpc=ecs_cluster.vpc,
                service=ecs_cluster.create_ecs_service(),
            )
        )

    def create_ecs_cluster(self):
        ecs_cluster = regular_constructs.autoscaling_ecs.AutoscalingEcsClusterConstruct(
            self, 'AutoscalingEcs',
        )
        ecs_cluster.create_autoscaling_group_provider(
            self.create_autoscaling_group(ecs_cluster.vpc)
        )
        return ecs_cluster

    @staticmethod
    def container_port():
        return 80

    def get_application_load_balancer_dns_name(self, vpc=None, service=None):
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
        return application_load_balancer.load_balancer_dns_name

    @staticmethod
    def create_health_check():
        return aws_cdk.aws_elasticloadbalancingv2.HealthCheck(
            interval=aws_cdk.Duration.seconds(60),
            path="/health",
            timeout=aws_cdk.Duration.seconds(5)
        )

    def get_port_mappings(self):
        return aws_cdk.aws_ecs.PortMapping(
            container_port=self.container_port(),
            host_port=8080,
            protocol=aws_cdk.aws_ecs.Protocol.TCP
        )

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