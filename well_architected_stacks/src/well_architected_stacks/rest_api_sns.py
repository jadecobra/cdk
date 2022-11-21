import constructs
import well_architected_constructs

from . import well_architected_stack


class RestApiSnsStack(well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        sns_topic_arn=None,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.rest_api_sns = well_architected_constructs.rest_api_sns.RestApiSns(
            self, 'RestApiSns',
            message="$util.urlEncode($context.path)",
            error_topic=self.error_topic,
            sns_topic_arn=sns_topic_arn,
        )
        self.create_cloudwatch_dashboard(
            *self.rest_api_sns.create_cloudwatch_widgets()
        )