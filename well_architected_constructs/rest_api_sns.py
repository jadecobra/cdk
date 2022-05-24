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
                deploy_options=aws_cdk.aws_apigateway.StageOptions(
                    metrics_enabled=True,
                    logging_level=aws_cdk.aws_apigateway.MethodLoggingLevel.INFO,
                    data_trace_enabled=True,
                    stage_name='prod'
                )
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