import aws_cdk
import constructs
import well_architected_stacks


class EcsClusterStack(well_architected_stacks.well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        vpc_id=None,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)
        self.vpc = self.get_vpc(vpc_id)
        self.cluster = self.create_ecs_cluster()

    def create_ecs_cluster(self):
        return aws_cdk.aws_ecs.Cluster(
            self, 'EcsCluster',
            vpc=self.vpc
        )