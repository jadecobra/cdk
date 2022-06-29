import aws_cdk
import constructs

class EcsCluster(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        vpc = aws_cdk.aws_ec2.Vpc(
            self, 'Vpc',
            max_azs=4,
        )

        # ecs_cluster = aws_cdk.aws_ecs.Cluster(
        #     self, 'EcsCluster',
        #     vpc=vpc
        # )
        ecs_cluster = self.create_ecs_cluster(vpc)

        ecs_cluster.add_asg_capacity_provider(
            aws_cdk.aws_ecs.AsgCapacityProvider(
                self, "AsgCapacityProvider",
                auto_scaling_group=aws_cdk.aws_autoscaling.AutoScalingGroup(
                    self, "AutoScalingGroup",
                    instance_type=aws_cdk.aws_ec2.InstanceType("t2.xlarge"),
                    machine_image=aws_cdk.aws_ecs.EcsOptimizedImage.amazon_linux2(),
                    associate_public_ip_address=True,
                    desired_capacity=3,
                    vpc=vpc,
                    vpc_subnets=aws_cdk.aws_ec2.SubnetSelection(
                        subnet_type=aws_cdk.aws_ec2.SubnetType.PUBLIC
                    ),
                )
            )
        )

    def create_ecs_cluster(self, vpc):
        return aws_cdk.aws_ecs.Cluster(
            self, 'EcsCluster',
            vpc=vpc
        )