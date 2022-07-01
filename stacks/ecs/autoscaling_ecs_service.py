import aws_cdk
import constructs
import regular_constructs.autoscaling_ecs
import well_architected


class AutoscalingEcsService(well_architected.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        container_image=None,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        ecs_cluster = self.create_ecs_cluster()
        ecs_cluster.create_ecs_service(
            network_mode=aws_cdk.aws_ecs.NetworkMode.AWS_VPC,
            security_group=self.create_security_group(ecs_cluster.vpc),
            container_image=container_image,
        )

    def create_ecs_cluster(self):
        ecs_cluster = regular_constructs.autoscaling_ecs.AutoscalingEcsClusterConstruct(
            self, 'AutoscalingEcs',
            network_mode=aws_cdk.aws_ecs.NetworkMode.AWS_VPC,
        )
        ecs_cluster.create_autoscaling_group_provider(
            self.create_autoscaling_group(ecs_cluster.vpc)
        )
        return ecs_cluster

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

    def create_autoscaling_group(self, vpc):
        return aws_cdk.aws_autoscaling.AutoScalingGroup(
            self, "DefaultAutoScalingGroup",
            instance_type=aws_cdk.aws_ec2.InstanceType("t2.micro"),
            machine_image=aws_cdk.aws_ecs.EcsOptimizedImage.amazon_linux2(),
            vpc=vpc,
        )