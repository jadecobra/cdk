from turtle import circle
import aws_cdk.pipelines as pipelines

# how to deploy in parallel
europe_wave = pipeline.add_wave('Europe')
europe_wave.add_stage(
    MyApplicationStage(
        self, 'Ireland',
        env=cdk.Environment(region='eu-west-1')
    )
)
europe_wave.add_stage(
    MyApplicationStage(
        self, 'Germany',
        env=cdk.Environment(region='eu-central-1')
    )
)

# how to deploy to other accounts and encrypt artifacts
pipeline = pipelines.CodePipeline(
    self, 'Pipeline',
    cross_account_keys=True,
    synth=pipelines.ShellStep(
        'Synth',
        input=pipelines.CodePipelineSource.connection(
            'my-org/my-app', 'main'
            connection_arn='arn:aws:codestar-connections:us-east-1:222222222222:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41'
        ),
        commands=[
            'npm ci',
            'npm run build',
            'npx cdk synth'
        ]
    )
)