import aws_cdk
import constructs

class AutoscalingEcs(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        self.vpc = self.create_vpc()
        self.ecs_cluster = self.create_ecs_cluster(self.vpc)
        self.ecs_cluster.add_asg_capacity_provider(
            self.create_autoscaling_group_provider(self.vpc)
        )

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

    def create_autoscaling_group_provider(self, vpc):
        return aws_cdk.aws_ecs.AsgCapacityProvider(
            self, "AsgCapacityProvider",
            auto_scaling_group=self.create_autoscaling_group(vpc)
        )