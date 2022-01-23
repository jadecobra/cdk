# The stacks for our app are minimally defined here.
# The internals of the stacks are not important
# excepyt that DatabaseStack exposes an attribute "table"
# for a database table it defines, and ComputeStack accepts
# a reference to this table in its properties

import aws_cdk.core as cdk
import aws_cdk.aws_dynamodb as dynamodb
import aws_cdk.pipelines as pipelines
import aws_cdk.aws_code_pipelines as codepipelines


class DatabaseStack(cdk.Stack):

    def __init__(self, scope, id):
        super().__init__(scope, id)
        self.table = dynamodb.Table(
            self, 'Table',
            partition_key=dynamodb.Attribute(
                name='id',
                type=dynamodb.AttributeType.STRING
            )
        )


class ComputeStack(cdk.Stack):

    def __init__(self, scope, id, *, table):
        super().__init__(scope, id)


class Application(pipelines.Stage):

    def __init__(self, scope, id, *, env=None, outdir=None):
        super().__init__(scope, id, env=env, outdir=outdir)

        database = DatabaseStack(self, 'Database')
        ComputeStack(self, 'Compute', table=database.table)


class PipelineStack(cdk.Stack):

    def __init__(
        self, scope, id, *, description=None, env=None, stackName=None, tags=None,
        synthesizer=None, terminationProtection=None, analyticsReporting=None
    ):
        super().__init__(
            scope, id, description=description, env=env, stackName=stackName, tags=tags,
            synthesizer=synthesizer, terminationProtection=terminationProtection,
            analyticsReporting=analyticsReporting
        )

        pipeline = pipelines.CodePipeline(
            self, 'Pipeline',
            synth=pipelines.ShellStep(
                'Synth',
                # Use a connection created using the AWS console to authenticate to GitHub
                # Other sources are vailable
                input=pipelines.CodePipelineSource.connection(
                    "my-org/my-app",
                    "main",
                    connection_arn="arn:aws:codestar-connections:us-east-1:234567890121:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41"
                ),
                commands=[
                    "npm ci",
                    "npm run build",
                    "npx cdk synth",
                ]
            )
        )

        pipeline.add_stage(
            Application(
                self, 'Prod',
                env=cdk.Environment(
                    account='123456789012',
                    region='us-west-1'
                )
            )
        )

# how to provision the pipeline
# cdk bootstrap
# git commit -a
# git push
# cdk deploy PipelineStack

# how to turn off self mutation
# Modern API
modern_pipeline = pipelines.CodePipeline(
    self, 'Pipeline',
    self_mutation=False,
    synth=pipelines.ShellStep(
        'Synth',
        input=pipelines.CodePipelineSource.connection(
            'my-org/my-app',
            'main',
            connection_arn='arn:aws:codestar-connections:us-east-1:234567890121:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41'
        ),
        commands=[
            'npm ci',
            'npm run build',
            'npx cdk synth',
        ]
    )
)

# Original API
cloud_assembly_artifact = codepipeline.Artifact()
original_pipeline = pipelines.CdkPipeline(
    self, 'Pipeline',
    self_mutating=False,
    cloud_assembly_artifact=cloud_assembly_artifact,
)