import aws_cdk
import constructs
import regular_constructs.autoscaling_ecs
import well_architected


class AutoscalingEcsCluster(well_architected.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        ecs_cluster = regular_constructs.autoscaling_ecs.AutoscalingEcsClusterConstruct(
            self, 'AutoscalingEcs',
        )
        ecs_cluster.create_autoscaling_group_provider(
            self.create_autoscaling_group(ecs_cluster.vpc)
        )

    def get_subnets(self):
        return aws_cdk.aws_ec2.SubnetSelection(
            subnet_type=aws_cdk.aws_ec2.SubnetType.PUBLIC
        )

    def create_autoscaling_group(self, vpc):
        return aws_cdk.aws_autoscaling.AutoScalingGroup(
            self, "AutoScalingGroup",
            instance_type=aws_cdk.aws_ec2.InstanceType("t2.micro"),
            machine_image=aws_cdk.aws_ecs.EcsOptimizedImage.amazon_linux2(),
            associate_public_ip_address=True,
            desired_capacity=3,
            vpc=vpc,
            vpc_subnets=self.get_subnets(),
        )