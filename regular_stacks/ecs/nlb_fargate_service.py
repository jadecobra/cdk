import aws_cdk
import constructs
import well_architected_stacks


class NlbFargateService(well_architected_stacks.well_architected_stack.Stack):

    def __init__(self, scope: constructs.Construct, id: str,
        container_image=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.nlb_fargate_service = aws_cdk.aws_ecs_patterns.NetworkLoadBalancedFargateService(
            self, "NlbEcsFargateService",
            assign_public_ip=True,
            vpc=self.get_vpc(),
            task_image_options=aws_cdk.aws_ecs_patterns.NetworkLoadBalancedTaskImageOptions(
                image=aws_cdk.aws_ecs.ContainerImage.from_registry(container_image)
            )
        )

        aws_cdk.CfnOutput(
            self, "LoadBalancerDNS",
            value=self.nlb_fargate_service.load_balancer.load_balancer_dns_name
        )
