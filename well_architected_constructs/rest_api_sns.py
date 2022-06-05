import aws_cdk
import constructs
from .rest_api import RestApiConstruct


class RestApiSnsConstruct(RestApiConstruct):

    def __init__(
        self, scope: constructs.Construct, id: str,
        error_topic=None,
        rest_api_name=None,
        api=None,
        request_templates=None,
        method=None,
        **kwargs,
    ):
        super().__init__(
            scope, id,
            error_topic=error_topic,
            api=aws_cdk.aws_apigateway.RestApi(
                scope, 'RestApi',
                rest_api_name=rest_api_name,
                deploy_options=self.get_stage_options(),
            ) if api is None else api,
            **kwargs,
        )
        self.add_method(
            method=method,
            path='SendEvent',
            uri='arn:aws:apigateway:us-east-1:sns:path//',
            success_response_templates={
                "message": 'Message added to SNS topic'
            },
            error_selection_pattern="Error",
            request_parameters={
                'integration.request.header.Content-Type': "'application/x-www-form-urlencoded'"
            },
            request_templates=request_templates,
        )