import aws_cdk
import constructs
import json

from .rest_api import RestApiConstruct


class RestApiSnsConstruct(RestApiConstruct):

    def __init__(
        self, scope: constructs.Construct, id: str,
        error_topic=None, api=None, **kwargs,
    ):
        super().__init__(
            scope, id,
            error_topic=error_topic,
            api=aws_cdk.aws_apigateway.RestApi(
                scope, 'RestApiSns',
                deploy_options=self.get_stage_options()
            ),
            **kwargs,
        )

    @staticmethod
    def get_stage_options():
        return aws_cdk.aws_apigateway.StageOptions(
            metrics_enabled=True,
            logging_level=aws_cdk.aws_apigateway.MethodLoggingLevel.INFO,
            data_trace_enabled=True,
            stage_name='prod'
        )

    def create_integration_response(
        self, status_code=None, response_templates=None,
        response_parameters=None, selection_pattern=None,
        separators=None
    ):
        return aws_cdk.aws_apigateway.IntegrationResponse(
            status_code=str(status_code),
            selection_pattern=selection_pattern,
            response_templates=self.create_json_template(
                json.dumps(response_templates, separators=separators)
            ),
            response_parameters=response_parameters,
        )

    def get_integration_responses(self):
        return [
            self.create_integration_response(
                status_code=200,
                response_templates={
                    "message": 'Message added to SNS topic'
                }
            ),
            self.create_integration_response(
                status_code=400,
                response_templates={
                    "message": "$util.escapeJavaScript($input.path('$.errorMessage'))",
                    "state": 'error',
                },
                selection_pattern="^\[Error\].*",
                separators=(',', ':'),
                response_parameters=self.create_response_parameters(
                    content_type=f"{self.content_type()}",
                    allow_origin="'*'",
                    allow_credentials="'true'",
                )
            )
        ]
