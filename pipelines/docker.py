import aws_cdk.pipelines as pipelines
import aws_cdk.

# how to use docker image assets
pipeline = pipelines.CodePipeline(
    self, 'PIpeline',
    synth=pipelines.ShellStep(
        'Synth',
        input=pipelines.CodePipelineSource.connection(
            'my-org/my-app',
            'main',
            connection_arn='arn:aws:codestar-connections:us-east-1:222222222222:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41',
        ),
        commands=[
            'npm ci',
            'npm run build',
            'npx cdk synth',
        ]
    ),
    docker_enabled_for_self_mutation=True,
)

pipeline.add_wave(
    'MyWave',
    post=[
        pipelines.CodeBuildStep(
            'RunApproval',
            commands=['command-from-image'],
            build_environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.from_asset(
                    self, 'Image', directory='./docker-image'
                )
            )
        )
    ]
)

# how to use bundled file assets
pipeline = pipelines.CodePipeline(
    self, 'Pipeline',
    synth=pipelines.CodePipelineSource.connection(
        'my-org/my-app',
        'main',
        connection_arn='arn:aws:codestar-connections:us-east-1:222222222222:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41',
    ),
    docker_enabled_for_synth=True,
)

# how to authenticate docker registries
import aws_cdk.aws_secretsmanager as secretsmanager
import aws_cdk.aws_ecr as ecr

docker_hub_secret = secretsmanager.Secret.from_secret_complete_arn(
    self, 'DHSecret', 'arn:aws:secretsmanager:us-east-1:222222222222:secret:my-secret-name/my-secret-version'
)
custom_registry_secret = secretsmanager.Secret.from_secret_complete_arn(
    self, 'CRSecret', 'arn:aws:secretsmanager:us-east-1:222222222222:secret:my-secret-name/my-secret-version'
)
repo1 = ecr.Repository(self, 'Repo1', 'arn:aws:ecr:us-east-1:123456789012:repository/Repo1')
repo2 = ecr.Repository(self, 'Repo2'. 'arn:aws:ecr:us-east-1:123456789012:repository/Repo2')

pipeline = pipelines.CodePipeline(
    self, 'Pipeline',
    docker_credentials=[
        pipelines.DockerCredential.docker_hub(docker_hub_secret),
        pipelines.DockerCredential.custom_registry('dockerregistry.example.com', custom_registry_secret),
        pipelines.DockerCredential.ecr([repo1, repo2])
    ],
    synth=pipelines.ShellStep(
        'Synth',
        input=pipelines.CodePipelineSource.connection(
            'my-org/my-app',
            'main',
            connection_arn='arn:aws:codestar-connections:us-east-1:234567890121:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41',
        ),
        commands=[
            'npm ci',
            'npm run build',
            'npx cdk synth',
        ]
    )
)

# how to limit the scope of credentials
docker_hub_secret = secretsmanager.Secret.from_secret_complete_arn(
    self, 'DHSecret', 'arn:aws:secretsmanager:us-east-1:222222222222:secret:my-secret-name/my-secret-version'
)
credentials = pipelines.DockerCredential.docker_hub(
    docker_hub_secret,
    usages=[pipelines.DockerCredentialUsage.ASSET_PUBLISHING]
)