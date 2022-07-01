import aws_cdk
import constructs
import regular_constructs.autoscaling_ecs

from aws_cdk import (
    aws_autoscaling as autoscaling,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    App, Stack
)


class Ec2ServiceWithTaskNetworking(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)


        vpc = ec2.Vpc(
            self, "Vpc",
            max_azs=2
        )

        cluster = aws_cdk.aws_ecs.Cluster(
            self, "awsvpc-ecs-demo-cluster",
            vpc=vpc
        )

        asg = aws_cdk.aws_autoscaling.AutoScalingGroup(
            self, "DefaultAutoScalingGroup",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ecs.EcsOptimizedImage.amazon_linux2(),
            vpc=vpc,
        )
        capacity_provider = aws_cdk.aws_ecs.AsgCapacityProvider(
            self, "AsgCapacityProvider",
            auto_scaling_group=asg
        )
        cluster.add_asg_capacity_provider(capacity_provider)

        # Create a task definition with its own elastic network interface
        task_definition = aws_cdk.aws_ecs.Ec2TaskDefinition(
            self, "nginx-awsvpc",
            network_mode=aws_cdk.aws_ecs.NetworkMode.AWS_VPC,
        )

        web_container = task_definition.add_container(
            "nginx",
            image=aws_cdk.aws_ecs.ContainerImage.from_registry("nginx:latest"),
            cpu=100,
            memory_limit_mib=256,
            essential=True
        )
        port_mapping = aws_cdk.aws_ecs.PortMapping(
            container_port=80,
            protocol=ecs.Protocol.TCP
        )
        web_container.add_port_mappings(port_mapping)

        # Create a security group that allows HTTP traffic on port 80 for our
        # containers without modifying the security group on the instance
        security_group = aws_cdk.aws_ec2.SecurityGroup(
            self, "nginx--7623",
            vpc=vpc,
            allow_all_outbound=False
        )
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(80)
        )

        # Create the service
        service = aws_cdk.aws_ecs.Ec2Service(
            self, "awsvpc-ecs-demo-service",
            cluster=cluster,
            task_definition=task_definition,
            security_groups=[security_group]
        )