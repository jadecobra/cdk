import aws_cdk
import constructs


class AutoscalingEcs(constructs.Construct):

    def __init__(
        self, scope: constructs.Construct, id: str, autoscaling_group=None,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)
        self.vpc = self.create_vpc()
        self.ecs_cluster = self.create_ecs_cluster(self.vpc)

    def create_vpc(self, max_azs=4):
        return aws_cdk.aws_ec2.Vpc(
            self, 'Vpc',
            max_azs=2,
        )

    def create_ecs_cluster(self, vpc):
        return aws_cdk.aws_ecs.Cluster(
            self, 'EcsCluster',
            vpc=vpc
        )

    def create_autoscaling_group(self, vpc):
        raise NotImplementedError

    def create_autoscaling_group_provider(self, autoscaling_group):
        if autoscaling_group:
            self.ecs_cluster.add_asg_capacity_provider(
                aws_cdk.aws_ecs.AsgCapacityProvider(
                    self, "AsgCapacityProvider",
                    auto_scaling_group=autoscaling_group
                )
            )