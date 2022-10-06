import constructs
import well_architected_constructs

from . import well_architected_stack


class RestApiSnsStack(well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        sns_topic=None, display_name=None,
        sns_topic_arn=None,
        error_topic=None,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)
        self.error_topic = self.create_error_topic()
        well_architected_constructs.rest_api_sns.RestApiSnsConstruct(
            self, 'RestApiSns',
            message="$util.urlEncode($context.path)",
            error_topic=self.error_topic,
            sns_topic_arn=sns_topic_arn,
        )