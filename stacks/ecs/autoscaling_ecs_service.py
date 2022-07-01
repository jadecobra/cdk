import aws_cdk
import constructs
import regular_constructs.autoscaling_ecs_cluster
import well_architected


class AutoscalingEcsService(well_architected.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        container_image=None,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        ecs_cluster = self.create_ecs_cluster()
        ecs_task_definition = self.create_task_definition()
        ecs_cluster.create_ecs_service(
            ecs_task_definition=ecs_task_definition,
            security_group=self.create_security_group(ecs_cluster.vpc),
        )

        self.create_container(
            ecs_task_definition=ecs_task_definition,
            container_image=container_image,
        )


    def create_ecs_cluster(self):
        ecs_cluster = regular_constructs.autoscaling_ecs_cluster.AutoscalingEcsClusterConstruct(
            self, 'AutoscalingEcs',
        )
        ecs_cluster.create_autoscaling_group_provider(
            self.create_autoscaling_group(ecs_cluster.vpc)
        )
        return ecs_cluster

    @staticmethod
    def get_port_mappings():
        return aws_cdk.aws_ecs.PortMapping(
            container_port=80,
            protocol=aws_cdk.aws_ecs.Protocol.TCP
        )

    def create_container(self, ecs_task_definition=None, container_image=None):
        ecs_task_definition.add_container(
            "Container",
            image=aws_cdk.aws_ecs.ContainerImage.from_registry(container_image),
            cpu=100,
            memory_limit_mib=256,
            essential=True
        ).add_port_mappings(
            self.get_port_mappings()
        )

    def create_task_definition(self):
        return aws_cdk.aws_ecs.Ec2TaskDefinition(
            self, "TaskDefinition",
            network_mode=aws_cdk.aws_ecs.NetworkMode.AWS_VPC,
        )

    def create_security_group(self, vpc):
        security_group = aws_cdk.aws_ec2.SecurityGroup(
            self, "SecurityGroup",
            vpc=vpc,
            allow_all_outbound=False
        )
        security_group.add_ingress_rule(
            aws_cdk.aws_ec2.Peer.any_ipv4(),
            aws_cdk.aws_ec2.Port.tcp(80)
        )
        return security_group

    def create_task_definition(self):
        return aws_cdk.aws_ecs.Ec2TaskDefinition(
            self, "TaskDefinition",
            network_mode=aws_cdk.aws_ecs.NetworkMode.AWS_VPC,
        )

    def create_autoscaling_group(self, vpc):
        return aws_cdk.aws_autoscaling.AutoScalingGroup(
            self, "DefaultAutoScalingGroup",
            instance_type=aws_cdk.aws_ec2.InstanceType("t2.micro"),
            machine_image=aws_cdk.aws_ecs.EcsOptimizedImage.amazon_linux2(),
            vpc=vpc,
        )