import aws_cdk.pipelines as pipelines

# using yarn
pipeline = pipelines.CodePipeline(
    self, 'Pipeline',
    synth=pipelines.ShellStep(
        'Synth',
        input=source,
        commands=[
            'yarn install --frozen-lockfile',
            'yarn build',
            'npx cdk synth',
        ]
    )
)

# python
pipeline = pipelines.CodePipeline(
    self, 'Pipeline',
    synth=pipelines.ShellStep(
        'Synth',
        input=source,
        commands=[
            'pip install -r requirements.txt',
            'npm install -g aws-cdk',
            'cdk synth',
        ]
    )
)

# java
pipeline = pipelines.CodePipeline(
    synth=pipelines.ShellStep(
        'Synth',
        input=source,
        comands=[
            'npm install -g aws-cdk',
            'cdk synth',
        ]
    )
)