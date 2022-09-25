import aws_cdk
import constructs
import well_architected_stacks


class NlbEc2Service(well_architected_stacks.well_architected_stack.Stack):

    def __init__(self, scope: constructs.Construct, id: str,
        container_image=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.nlb_ec2_service = aws_cdk.aws_ecs_patterns.NetworkLoadBalancedEc2Service(
            self, "NlbEc2Service",
            desired_count=1,
            cpu=256,
            memory_limit_mib=512,
            public_load_balancer=True,
            vpc=self.get_vpc(),
            task_image_options=aws_cdk.aws_ecs_patterns.NetworkLoadBalancedTaskImageOptions(
                image=aws_cdk.aws_ecs.ContainerImage.from_registry(container_image)
            )
        )

        aws_cdk.CfnOutput(
            self, "LoadBalancerDNS",
            value=self.nlb_ec2_service.load_balancer.load_balancer_dns_name
        )
