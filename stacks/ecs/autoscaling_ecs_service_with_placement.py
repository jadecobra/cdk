import aws_cdk
import constructs
import regular_constructs.autoscaling_ecs


class AutoscalingEcsServiceWithPlacement(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, id: str,
        container_image=None,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        ecs_cluster = self.create_ecs_cluster()
        ecs_service = ecs_cluster.create_ecs_service(
            container_image=container_image,
            placement_constraints=[
                aws_cdk.aws_ecs.PlacementConstraint.distinct_instances()
            ]
        )

        ecs_service.add_placement_strategies(
            aws_cdk.aws_ecs.PlacementStrategy.packed_by(
                aws_cdk.aws_ecs.BinPackResource.MEMORY
            )
        )
        ecs_service.add_placement_strategies(
            aws_cdk.aws_ecs.PlacementStrategy.spread_across(
                aws_cdk.aws_ecs.BuiltInAttributes.AVAILABILITY_ZONE
            )
        )

    def create_autoscaling_group(self, vpc):
        return aws_cdk.aws_autoscaling.AutoScalingGroup(
            self, "AutoScalingGroup",
            instance_type=aws_cdk.aws_ec2.InstanceType("t2.micro"),
            machine_image=aws_cdk.aws_ecs.EcsOptimizedImage.amazon_linux2(),
            vpc=vpc,
        )

    def create_ecs_cluster(self):
        ecs_cluster = regular_constructs.autoscaling_ecs.AutoscalingEcsClusterConstruct(
            self, 'AutoscalingEcs',
        )
        ecs_cluster.create_autoscaling_group_provider(
            self.create_autoscaling_group(ecs_cluster.vpc)
        )
        return ecs_cluster