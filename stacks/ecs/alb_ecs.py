import aws_cdk
import constructs
import regular_constructs

class AlbEcs(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # vpc = aws_cdk.aws_ec2.Vpc(
        #     self, "MyVpc",
        #     max_azs=2
        # )

        # ecs_cluster = aws_cdk.aws_ecs.Cluster(
        #     self, 'EcsCluster',
        #     vpc=vpc
        # )
        ecs_cluster = regular_constructs.autoscaling_ecs.AutoscalingEcsConstruct(
            self, 'AutoscalingEcs',
        )
        ecs_cluster.create_autoscaling_group_provider(
            self.create_autoscaling_group(ecs_cluster.vpc)
        )

        autoscaling_group = aws_cdk.aws_autoscaling.AutoScalingGroup(
            self, "AutoScalingGroup",
            instance_type=aws_cdk.aws_ec2.InstanceType.of(
                aws_cdk.aws_ec2.InstanceClass.BURSTABLE3,
                aws_cdk.aws_ec2.InstanceSize.MICRO
            ),
            machine_image=aws_cdk.aws_ecs.EcsOptimizedImage.amazon_linux2(),
            vpc=vpc,
        )

        ecs_cluster.add_asg_capacity_provider(
            aws_cdk.aws_ecs.AsgCapacityProvider(
                self, "AsgCapacityProvider",
                auto_scaling_group=autoscaling_group
            )
        )

        ecs_task_definition = aws_cdk.aws_ecs.Ec2TaskDefinition(
            self, "TaskDef"
        )
        ecs_container = ecs_task_definition.add_container(
            "web",
            image=aws_cdk.aws_ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
            memory_limit_mib=256
        )
        ecs_port_mapping = aws_cdk.aws_ecs.PortMapping(
            container_port=80,
            host_port=8080,
            protocol=aws_cdk.aws_ecs.Protocol.TCP
        )
        ecs_container.add_port_mappings(ecs_port_mapping)

        service = aws_cdk.aws_ecs.Ec2Service(
            self, "Service",
            cluster=ecs_cluster,
            task_definition=ecs_task_definition
        )

        application_load_balancer = aws_cdk.aws_elasticloadbalancingv2.ApplicationLoadBalancer(
            self, "LB",
            vpc=vpc,
            internet_facing=True
        )
        listener = application_load_balancer.add_listener(
            "PublicListener",
            port=80,
            open=True
        )

        health_check = aws_cdk.aws_elasticloadbalancingv2.HealthCheck(
            interval=aws_cdk.Duration.seconds(60),
            path="/health",
            timeout=aws_cdk.Duration.seconds(5)
        )

        # Attach ALB to ECS Service
        listener.add_targets(
            "ECS",
            port=80,
            targets=[service],
            health_check=health_check,
        )

        aws_cdk.CfnOutput(
            self, "LoadBalancerDNS",
            value=application_load_balancer.load_balancer_dns_name
        )