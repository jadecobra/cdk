import aws_cdk
import aws_cdk.aws_batch_alpha
import constructs
import well_architected_stacks


class BatchEC2Stack(well_architected_stacks.well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        container_name=None,
        number_of_environments=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        self.vpc = self.get_vpc()
        self.container_name = container_name

        batch_compute_environments = self.create_batch_compute_environments(number_of_environments=)
        # batch_compute_environments = [
        #     aws_cdk.aws_batch_alpha.JobQueueComputeEnvironment(
        #         compute_environment=self.create_compute_environment(number),
        #         order=number
        #     ) for number in range(number_of_environments)
        # ]

        self.batch_queue = self.create_batch_queue(batch_compute_environments)
        self.batch_job_definition = self.create_batch_job_definition()

        aws_cdk.CfnOutput(self, "BatchJobQueue",value=self.batch_queue.job_queue_name)
        aws_cdk.CfnOutput(self, "JobDefinition",value=self.batch_job_definition.job_definition_name)

    def create_batch_compute_environments(self, number_of_environments):
        return [
            aws_cdk.aws_batch_alpha.JobQueueComputeEnvironment(
                compute_environment=self.create_compute_environment(number),
                order=number
            ) for number in range(number_of_environments)
        ]

    def create_batch_queue(self, compute_environments):
        return aws_cdk.aws_batch_alpha.JobQueue(
            self, "JobQueueArm64",
            compute_environments=compute_environments
        )

    @staticmethod
    def get_instance_types():
        return [
            aws_cdk.aws_ec2.InstanceType("a1.medium"),
            aws_cdk.aws_ec2.InstanceType("a1.large")
        ]

    @staticmethod
    def get_subnets():
        return aws_cdk.aws_ec2.SubnetSelection(
            subnet_type=aws_cdk.aws_ec2.SubnetType.PRIVATE_WITH_NAT
        )

    @staticmethod
    def get_ami():
        return aws_cdk.aws_ecs.EcsOptimizedImage.amazon_linux2(
            aws_cdk.aws_ecs.AmiHardwareType.ARM
        )

    def get_container(self):
        return aws_cdk.aws_batch_alpha.JobDefinitionContainer(
            image=aws_cdk.aws_ecs.ContainerImage.from_registry(
                self.container_name
            ),
            command=["sleep", "60"],
            memory_limit_mib=512,
            vcpus=1
        )

    def create_batch_job_definition(self):
        return aws_cdk.aws_batch_alpha.JobDefinition(
            self, "MyJobDefArm64",
            job_definition_name="CDKJobDefArm64",
            container=self.get_container(),
        )

    def create_compute_environment(self, number):
        return aws_cdk.aws_batch_alpha.ComputeEnvironment(
            self, f"BatchARM64Env{number}",
            compute_resources=aws_cdk.aws_batch_alpha.ComputeResources(
                type=aws_cdk.aws_batch_alpha.ComputeResourceType.SPOT,
                bid_percentage=75,
                instance_types=self.get_instance_types(),
                image=self.get_ami(),
                vpc_subnets=self.get_subnets(),
                vpc=self.vpc
            )
        )