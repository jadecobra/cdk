import aws_cdk.pipelines as pipelines
import aws_cdk.aws_codecommit as codecommit

# git
# add connection in AWS Console
pipelines.CodePipelineSource.connection(
    'org/repo',
    'branch',
    connection_arn='arn:aws:codestar-connections:us-east-1:123456789012:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41',
)

# github with OAuth with Personal Access Token
# scopes - repo, admin:repo_hook
pipelines.CodePipelineSource.git_hub(
    'org/repo',
    'branch',
    authentication=cdk.SecretValue.secrets_manager('token-name')
)

# CodeCommit
repository = codecommit.Repository.from_repository_name(
    self, 'Repository',
    'repository_name'
)
pipelines.CodePipelineSource.code_commit(repository, 'main')

# s3
bucket = s3.Bucket.from_bucket_name(self, 'Bucket', 'bucket-name')
pipelines.CodePipelineSource.s3(bucket, 'path/to/source.zip')

