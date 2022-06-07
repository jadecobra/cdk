import constructs

import well_architected
import well_architected_constructs.rest_api_sns


class SnsRestApi(well_architected.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        sns_topic=None, display_name=None,
        error_topic=None,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)
        well_architected_constructs.rest_api_sns.RestApiSnsConstruct(
            self, 'SnsRestApi',
            message="$util.urlEncode($context.path)",
            error_topic=error_topic,
        )