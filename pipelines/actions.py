import aws_cdk.aws_codepipeline_actiosn as codepipeline_actions
import aws_cdk.aws_codepipeline as codepipeline

# how to add an action to a stage
pipeline = codepipeline.Pipeline(self, 'Pipeline')
source = pipeline.add_stage(stage_name='Source')
source.add_action(codepipeline_actions.CodeCommitSourceAction())

# how to make a custom action registration
codepipeline.CustomActionRegistration(
    self, 'GenericGitSourceProviderResource',
    category=codepipeline.ActionCategory.SOURCE,
    artifact_bounds=codepipeline.ActionartifactBounds(
        min_inputs=0,
        max_inputs=0,
        min_outputs=1,
        max_outputs=1
    ),
    provider='GenericGitSource',
    version='1',
    entity_url='https://docs.aws.amazon.com/codepipeline/latest/userguide/actions-create-custom-action.html',
    execution_url='https://docs.aws.amazon.com/codepipeline/latest/userguide/actions-create-custom-action.html',
    action_properties=[
        codepipeline.CustomactionProperty(
            name='Branch',
            required=True,
            key=False,
            secret=False,
            queryable=False,
            description='Git brnach to pull',
            type='String'
        ),
        codepipeline.CustomActionProperty(
            name='GitUrl',
            required=True,
            key=False,
            secret=False,
            queryable=False,
            description='SSH git clone URL',
            type='String'
        )
    ]
)