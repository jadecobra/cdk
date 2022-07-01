import aws_cdk
import constructs
import regular_constructs.autoscaling_ecs
import well_architected


class Ec2ServiceWithTaskNetworking(well_architected.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        container_image=None,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        ecs_cluster = regular_constructs.autoscaling_ecs.AutoscalingEcsConstruct(
            self, 'AutoscalingEcs',
        )
        ecs_cluster.create_autoscaling_group_provider(
            self.create_autoscaling_group(ecs_cluster.vpc)
        )

        task_definition = aws_cdk.aws_ecs.Ec2TaskDefinition(
            self, "nginx-awsvpc",
            network_mode=aws_cdk.aws_ecs.NetworkMode.AWS_VPC,
        )

        web_container = task_definition.add_container(
            "nginx",
            image=aws_cdk.aws_ecs.ContainerImage.from_registry("nginx:latest"),
            cpu=100,
            memory_limit_mib=256,
            essential=True
        )
        port_mapping = aws_cdk.aws_ecs.PortMapping(
            container_port=80,
            protocol=aws_cdk.aws_ecs.Protocol.TCP
        )
        web_container.add_port_mappings(port_mapping)

        self.create_ecs_service(
            ecs_cluster=ecs_cluster.ecs_cluster,
            ecs_task_definition=task_definition,
            security_group=self.create_security_group(ecs_cluster.vpc),
        )

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

    def create_ecs_service(self, ecs_cluster=None, ecs_task_definition=None, security_group=None):
        return aws_cdk.aws_ecs.Ec2Service(
            self, "Service",
            cluster=ecs_cluster,
            task_definition=ecs_task_definition,
            security_groups=[security_group]
        )

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