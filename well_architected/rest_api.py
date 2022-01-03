from aws_cdk.core import Stack, Construct
from aws_cdk.aws_logs import LogGroup
from aws_cdk.aws_lambda import Function
from api_gateway_cloudwatch import ApiGatewayCloudWatch
from aws_cdk.aws_sns import ITopic

import aws_cdk.aws_apigateway as api_gateway


class LambdaRestAPIGateway(Stack):

    def __init__(self, scope: Construct, id: str, lambda_function: Function, error_topic:ITopic=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.rest_api = self.create_rest_api()
        self.create_api_method(
            resource=self.create_api_resource(self.rest_api),
            lambda_function=lambda_function,

        )
        self.resource_arn = f"arn:aws:apigateway:{self.region}::/restapis/{self.rest_api.rest_api_id}/stages/{self.rest_api.deployment_stage.stage_name}"

        self.api_gateway_cloudwatch_widgets = ApiGatewayCloudWatch(
            self, 'ApiGatewayCloudWatch',
            api_id=self.rest_api.rest_api_id,
            error_topic=error_topic,
        ).api_gateway_cloudwatch_widgets

    def method_origin(self):
        return 'method.response.header.Access-Control-Allow-Origin'

    def status_code(self):
        return '200'

    def create_method_responses(self):
        return [
            api_gateway.MethodResponse(
                status_code=self.status_code(),
                response_parameters={
                    self.method_origin(): True
                }
            )
        ]

    def create_api_method(self, resource=None, lambda_function=None):
        return resource.add_method(
            'GET', self.create_lambda_integration(lambda_function),
            method_responses=self.create_method_responses()
        )

    def create_integration_responses(self):
        return [
            api_gateway.IntegrationResponse(
                status_code=self.status_code(),
                response_parameters={
                    self.method_origin(): "'*'"
                }
            )
        ]

    def create_lambda_integration(self, lambda_function):
        return api_gateway.LambdaIntegration(
            lambda_function,
            proxy=False,
            integration_responses=self.create_integration_responses()
        )

    def create_api_resource(self, api):
        return api.root.add_resource('hello')

    def create_log_group(self):
        return LogGroup(self, "helloAPILogs")

    def method_deployment_options(self):
        return {
            # This special path applies to all resource paths and all HTTP methods
            "/*/*": api_gateway.MethodDeploymentOptions(
                throttling_rate_limit=100,
                throttling_burst_limit=200
            )
        }

    def deploy_options(self):
        return api_gateway.StageOptions(
            method_options=self.method_deployment_options(),
            access_log_format=api_gateway.AccessLogFormat.clf(),
            access_log_destination=api_gateway.LogGroupLogDestination(
                self.create_log_group()
            ),
        )

    def create_rest_api(self):
        return api_gateway.RestApi(
            self, 'LambdaAPIGateway',
            rest_api_name='hello',
            endpoint_types=[api_gateway.EndpointType.REGIONAL],
            deploy_options=self.deploy_options(),
        )