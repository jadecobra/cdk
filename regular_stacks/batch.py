import aws_cdk
import aws_cdk.aws_batch_alpha
import constructs
import well_architected_stacks


class BatchEC2Stack(well_architected_stacks.well_architected_stack.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.vpc = self.get_vpc()
        batch_compute_environment = []
        count = 3

        # For loop to create Batch Compute Environments
        for i in range(count):
            batch_environment = aws_cdk.aws_batch_alpha.ComputeEnvironment(
                self, f"BatchARM64Env{i}",
                compute_resources=aws_cdk.aws_batch_alpha.ComputeResources(
                type=aws_cdk.aws_batch_alpha.ComputeResourceType.SPOT,
                bid_percentage=75,
                instance_types=[
                    aws_cdk.aws_ec2.InstanceType("a1.medium"),
                    aws_cdk.aws_ec2.InstanceType("a1.large")
                ],
                image=aws_cdk.aws_ecs.EcsOptimizedImage.amazon_linux2(
                    aws_cdk.aws_ecs.AmiHardwareType.ARM
                ),
                vpc_subnets=aws_cdk.aws_ec2.SubnetSelection(
                    subnet_type=aws_cdk.aws_ec2.SubnetType.PRIVATE_WITH_NAT
                ),
                vpc=self.vpc
                )
            )

            batch_compute_environment.append(
                aws_cdk.aws_batch_alpha.JobQueueComputeEnvironment(
                    compute_environment=batch_environment,
                    order=i
                )
            )

        self.batch_queue = aws_cdk.aws_batch_alpha.JobQueue(
            self, "JobQueueArm64",
            compute_environments=batch_compute_environment
        )

        self.batch_job_definition = aws_cdk.aws_batch_alpha.JobDefinition(
            self, "MyJobDefArm64",
            job_definition_name="CDKJobDefArm64",
            container=aws_cdk.aws_batch_alpha.JobDefinitionContainer(
                image=aws_cdk.aws_ecs.ContainerImage.from_registry(
                    "public.ecr.aws/amazonlinux/amazonlinux:latest"
                ),
                command=["sleep", "60"],
                memory_limit_mib=512,
                vcpus=1
            ),
        )

        aws_cdk.CfnOutput(self, "BatchJobQueue",value=self.batch_queue.job_queue_name)
        aws_cdk.CfnOutput(self, "JobDefinition",value=self.batch_job_definition.job_definition_name)


# app = App()
# BatchEC2Stack(app, "BatchEC2Stack")
# app.synth()