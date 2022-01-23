import aws_cdk.pipeline as pipelines
# how to setup an npm based project
# source: pipelines.IFileSetProducer
# the repository source
pipeline = pipelines.CodePipeline(
    self, 'Pipeline',
    synth=pipelines.ShellStep(
        'Synth',
        input=source,
        commands=[
            'npm ci',
            'npm run build',
            'npx cdk synth'
        ]
    )
)

# how to specify the primary output directory
pipeline = pipelines.CodePipeline(
    self, 'Pipeline',
    synth=pipelines.ShellStep(
        'Synth',
        input=source,
        commands=[
            'cd sub_directory',
            'npm ci',
            'npm run build',
            'npx cdk synth',
        ],
        primary_output_directory='sub_directory/cdk.out'
    )
)
