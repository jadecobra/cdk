import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_codebuild as codebuild
import aws_cdk.core as cdk

# vpc: ec2.Vpc
# security_group: ec2.SecurityGroup

pipelines.CodeBuildStep(
    'Synth',
    commands=[],
    env={},

    primary_output_directory='cdk.out',
    proejct_name='MyProject',
    partial_build_spec=codebuild.BuildSpec.from_object({
        'version': '0.2',
    })

    build_environment=codebuild.BuildEnvironment(
        compute_type=codebuild.ComputeType.LARGE
    ),
    timeout=cdk.Duration.minutes(90)

    vpc=vpc,
    security_groups=[security_group],
    subnet_selection=ec2.SubnetSelection(
        subnet_type=ec2.SubnetType.PRIVATE
    )

    role_policy_statements=[
        iam.PolicyStatement()
    ]
)

# using defaults for CodeBuild
pipelines.CodeBuildStep(
    self, 'Pipeline',
    synth=pipeline.ShellStep(
        'Synth',
        input=pipelines.CodePipelineSource.connection(
            'my-org/my-app',
            'main',
            connection_arn='arn:aws:codestar-connections:us-east-1:222222222222:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41'
        ),
        commands=[
            'npm ci',
            'npm run build',
            'npx cdk synth',
        ]
    ),

    code_build_defaults=pipelines.CodeBuildOptions(
        partial_build_spec=codebuild.BuildSpec.from_object({
            'version': '0.2'
        }),

        build_environment=codebuild.BuildEnvironment(
            compute_type=codebuild.ComputeType.LARGE
        ),

        vpc=vpc
        subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE),
        security_groups=[security_group],

        role_policy=[iam.PolicyStatement()]
    ),

    synth_code_build_defaults=pipelines.CodeBuildOptions(),
    asset_publishing_code_build_defaults=pipelines.CodeBuildOptions(),
    self_mutation_code_build_defaults=pipelines.CodeBuildOptions(),
)