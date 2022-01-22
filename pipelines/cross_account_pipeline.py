import aws_cdk.aws_codepipeline as codepipeline
import aws_cdk.aws_codepipeline_actions as codepipeline_actions
import aws_cdk.aws_s3 as s3

# how to deploy to an imported S3 bucket from a different AWS account
pipeline = codepipeline.Pipeline(self, 'MyFirstPipeline')
stage = pipeline.add_stage(stage_name='Stage')
stage.add_action(
    codepipeline_actions.S3DeployAcion(
        bucket=s3.Bucket.from_bucket_attributes(
            self, 'Bucket',
            account='123456789012',
        ),
        input=input,
        action_name='s3-deploy-action',
    )
)

# how to deploy an action that does not accept a resource
stage.add_action(
    codepipleine_actions.CloudFormationCreateUpdateStackAction(
        account='123456789012',
        template_path=template_path,
        admin_permissions=False,
        stack_name=Stack.of(self).stack_name,
        action_name='cloudformation-create-update'
    )
)

# how to explicitly pass a role when creating an action
stage.add_action(
    codepipeline_actions.CloudFormationCreateUpdateStackAction(
        template_path=template_path,
        admin_permissions=False,
        stack_name=Stack.of(self).stack_name,
        action_name='cloudformation-create-update',
        role=iam.Role.from_role_arn(
            self, 'ActionRole',
            'arn:aws:iam::123456789012:role/ActionRole'
        )
    )
)