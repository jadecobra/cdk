import aws_cdk.aws_codepipeline as codepipeline
import aws_cdk.aws_events_targets as targets
import aws_cdk.aws_events as events
import aws_cdk.core as cdk

# how to schedule a pipeline
pipeline = codepipeline.Pipeline(self, 'Pipeline')
rule = events.rule(
    self, 'Daily',
    schedule=events.Schedule.rate(cdk.Duration.days(1))
)
rule.add_target(targets.CodePipeline(pipeline))

# how to define events rules for pipeline emitted events
pipeline = codepipeline.Pipeline(self, 'Pipeline')
pipeline.on_state_change('PipelineStateChange', target=target)

stage = pipeline.add_stage(stage_name='Stage')
stage.on_state_change('StageStateChange', target=target)

action = stage.add_action(action_name='Action')
action.on_state_change('ActionStateChange', target=target)