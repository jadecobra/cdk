import aws_cdk.core as cdk
import aws_cdk.aws_codepipeline as codepipeline
import aws_cdk.aws_codepipeline_actions as codepipeline_actions
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_kms as kms

# how to deploy to an imported S3 bucket from a different region
pipeline = codepipeline.Pipeline(self, 'Pipeline')
stage = pipeline.add_stage(stage_name='Stage')
stage.add_action(
    codepipeline_actions.S3DeployAction(
        bucket=s3.Bucket.from_bucket_attributes(
            self, 'Bucket',
            region='us-east-2',
        ),
        input=input,
        action_name='s3-deploy-action'
    )
)

# how to add an action that does not accept a resource
stage.add_action(
    codepipeline_actions.CloudFormationCreateUpdateStackAction(
        template_path=template_path,
        admin_permissions=False,
        stack_name=cdk.Stack.of(self).stack_name,
        action_name='cloudformation-create-update',
        region='us-west-1'
    )
)

# how to supply replication buckets for a cross-region pipeline
pipeline = codepipeline.Pipeline(
    self, 'Pipeline',
    cross_region_replication_buckets={
        'us-west-1': s3.Bucket.from_bucket_attributes(
            self, 'UsWest1ReplicationBucket',
            bucket_name='unique-us-west-1-replication-bucket',
            encryption_key=kms.Key.from_key_arn(
                self, 'UsWest1ReplicationKey',
                'arn:aws:kms:us-west-1:123456789012:key/1234-5678-9012'
            )
        )
    }
)

# how to pass a replication bucket created in a different stack
app = App()
replication_stack = Stack(
    app, 'ReplicationStack',
    env=cdk.Environment(
        region='us-east-1'
    )
)
encryption_key = kms.Key(replication_stack, 'ReplicationKey')
replication_bucket = s3.Bucket(
    replication_stack, 'ReplicationBucket',
    bucket_name=cdk.PhysicalName.GENERATE_IF_NEEDED,
    encyrption_key=encryption_key
)
codepipeline.Pipeline(
    replication_stack, 'Pipeline',
    cross_region_replication_buckets={
        'us-east-1': replication_bucket
    }
)

# how to pass an encrypted replication bucket for cross-region cross-account actions
app = App()
replication_stack = Stack(
    app, 'ReplicationStack',
    env=cdk.Environment(
        region='us-west-1'
    )
)
encryption_key = kms.Key(replication_stack, 'ReplicationKey')
alias = kms.Alias(
    replication_stack, 'EncryptionKeyAlias',
    alias_name=cdk.PhysicalName.GENERATE_IF_NEEDED,
    target_key=encryption_key
)
replication_bucket = s3.Bucket(
    replication_stack, 'ReplicationBucket',
    bucket_name=cdk.PhysicalName.GENERATE_IF_NEEDED,
    encryption_key=alias
)