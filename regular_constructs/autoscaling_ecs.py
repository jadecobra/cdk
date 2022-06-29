import aws_cdk
import constructs


class AutoscalingEcsConstruct(constructs.Construct):

    def __init__(
        self, scope: constructs.Construct, id: str,
        vpc=None,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)
        self.vpc = self.get_vpc(vpc)
        self.ecs_cluster = self.create_ecs_cluster(self.vpc)

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