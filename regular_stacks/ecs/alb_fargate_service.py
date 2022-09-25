import aws_cdk
import constructs
import well_architected_stacks


class AlbFargateService(well_architected_stacks.well_architected_stack.Stack):

    def __init__(self, scope: constructs.Construct, id: str,
        container_image=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.Alb_fargate_service = aws_cdk.aws_ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "AlbEcsFargateService",
            assign_public_ip=True,
            vpc=self.get_vpc(),
            task_image_options=aws_cdk.aws_ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=aws_cdk.aws_ecs.ContainerImage.from_registry(container_image)
            )
        )

        aws_cdk.CfnOutput(
            self, "LoadBalancerDNS",
            value=self.Alb_fargate_service.load_balancer.load_balancer_dns_name
        )
