import aws_cdk
import constructs
import well_architected_stacks

from . import autoscaling_ecs



class AutoscalingEcsService(well_architected_stacks.well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        container_image=None,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        autoscaling_ecs_cluster = autoscaling_ecs.AutoscalingEcsClusterConstruct(
            self, 'AutoscalingEcs',
        )
        autoscaling_ecs_cluster.create_ecs_service(
            network_mode=aws_cdk.aws_ecs.NetworkMode.AWS_VPC,
            security_group=self.create_security_group(autoscaling_ecs_cluster.vpc),
            container_image=container_image,
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