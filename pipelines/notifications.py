import aws_cdk.aws_codepipeline as codepipeline
import aws_cdk.aws_chatbot as chatbot

# how to define codestar notifications rules for pipelines
pipeline = codepipeline.Pipeline(self, 'Pipeline')
target = chatbot.SlackChannelConfiguration(
    self, 'SlackChannel',
    slack_channel_configuration_name='SlackChannelConfigurationName',
    slack_workspace_id='SlackWorkspaceId',
    slack_channel_id='SlackChannelId'
)
rule = pipeline.notify_on_execution_state_change('NotifyOnExecutionStateChange', target=target)