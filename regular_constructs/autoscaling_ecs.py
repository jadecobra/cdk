import aws_cdk
import constructs


class AutoscalingEcsClusterConstruct(constructs.Construct):

    def __init__(
        self, scope: constructs.Construct, id: str,
        vpc=None,
        network_mode=None,
        container_image=None,
        create_service=True,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)
        self.vpc = self.get_vpc(vpc)
        self.ecs_cluster = self.create_ecs_cluster(self.vpc)
        self.ecs_task_definition = self.create_task_definition(network_mode) if create_service else None
        self.create_container(container_image)

    def get_vpc(self, vpc=None):
        if vpc:
            return vpc
        else:
            return aws_cdk.aws_ec2.Vpc(
                self, 'Vpc',
                max_azs=2,
            )

    def create_ecs_cluster(self, vpc):
        return aws_cdk.aws_ecs.Cluster(
            self, 'EcsCluster',
            vpc=vpc
        )

    def create_autoscaling_group_provider(self, autoscaling_group):
        if autoscaling_group:
            self.ecs_cluster.add_asg_capacity_provider(
                aws_cdk.aws_ecs.AsgCapacityProvider(
                    self, "AsgCapacityProvider",
                    auto_scaling_group=autoscaling_group
                )
            )

    def create_ecs_service(self, security_group=None):
        return aws_cdk.aws_ecs.Ec2Service(
            self, "Service",
            cluster=self.ecs_cluster,
            task_definition=self.ecs_task_definition if self.ecs_task_definition else None,
            security_groups=[security_group] if security_group else None,
        )

    def create_task_definition(self, network_mode=None):
        return aws_cdk.aws_ecs.Ec2TaskDefinition(
            self, "TaskDefinition",
            network_mode=network_mode
        )

    @staticmethod
    def get_port_mappings():
        return aws_cdk.aws_ecs.PortMapping(
            container_port=80,
            protocol=aws_cdk.aws_ecs.Protocol.TCP
        )

    def create_container(self, container_image=None):
        if container_image:
            self.ecs_task_definition.add_container(
                "Container",
                image=aws_cdk.aws_ecs.ContainerImage.from_registry(container_image),
                cpu=100,
                memory_limit_mib=256,
                essential=True,
            ).add_port_mappings(
                self.get_port_mappings()
            )
