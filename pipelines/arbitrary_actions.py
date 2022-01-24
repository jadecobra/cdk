import aws_cdk.pipelines as pipelines
import aws_cdk.aws_codepipeline_actions as codepipeline_actions

# how to add a jenkins step
class MyJenkinsStep(pipelines.Steppipelines.ICodePipelineActionFactory):

    def __init__(self, provider, input):
        super().__init__('MyJenkinsStep')

    def produce_action(
        self, stage, *, scope, actionName, runOrder, artifacts,
        fallbackArtifact=None, pipeline, codeBuildDefaults=None,
        beforeSelfMutation=None
    ):
        stage.add_action(
            codepipeline_actions.JenkinsAction(
                action_name=action_name,
                run_order=run_order,
                type=codepipeline_actions.JenkinsActionType.TEST,
                jenkins_provider=self.provider
            )
        )
        return pipelines.CodePipelineActionFactoryResult(run_orders_consumed=1)