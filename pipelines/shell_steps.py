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

# Additional Inputs
prebuild = pipelines.ShellStep(
    input=pipelines.CodePipelineSource.git_hub('myorg/repo1', 'main'),
    primary_output_directory='./build',
    commands=['./build.sh']
)

pipeline = pipelines.CodePipeline(
    self, 'Pipeline',
    synth=pipelines.ShellStep(
        'Synth',
        input=pipelines.CodePipelineSource.git_hub('myorg/repo2', 'main')
        additional_inputs={
            'subdir': pipelines.CodePipelineSource.git_hub('myorg/repo3', 'main'),
            '../siblingdir': prebuild,
        },
        commands=['./build.sh']
    )
)