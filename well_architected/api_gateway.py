from aws_cdk.core import Stack, Construct, Duration
from aws_cdk.aws_logs import LogGroup
from aws_cdk.aws_lambda import Function, Code, Runtime

import aws_cdk.aws_apigateway as api_gateway



class LambdaAPIGateway(Stack):


    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.rest_api = self.create_rest_api()
        self.resource = self.create_resource()
        self.create_api_method(self.create_lambda_function())

        self.resource_arn = f"arn:aws:apigateway:{self.region}::/restapis/{self.rest_api.rest_api_id}/stages/{self.rest_api.deployment_stage.stage_name}"

    def create_api_method(self, lambda_function):
        return self.resource.add_method(
            'GET', self.create_lambda_integration(lambda_function),
            method_responses=[
                api_gateway.MethodResponse(
                    status_code='200',
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': True
                    }
                )
            ]
        )

    def create_lambda_integration(self, lambda_function):
        return api_gateway.LambdaIntegration(
            lambda_function,
            proxy=False,
            integration_responses=[
                api_gateway.IntegrationResponse(
                    status_code='200',
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': "'*'"
                    }
                )
            ]
        )

    def create_resource(self):
        return self.rest_api.root.add_resource('hello')

    def create_lambda_function(self):
        return Function(
            self, "hello",
            runtime=Runtime.PYTHON_3_8,
            handler='hello.lambda_handler',
            code=Code.from_asset("lambda_functions"),
            timeout=Duration.seconds(60)
        )

    def create_log_group(self):
        return LogGroup(self, "helloAPILogs")

    def create_rest_api(self):
        return api_gateway.RestApi(
            self, 'LambdaAPIGateway',
            rest_api_name='hello',
            endpoint_types=[api_gateway.EndpointType.REGIONAL],
            deploy_options=api_gateway.StageOptions(
                access_log_destination=api_gateway.LogGroupLogDestination(
                    self.create_log_group()
                ),
                access_log_format=api_gateway.AccessLogFormat.clf(),
                method_options={
                    # This special path applies to all resource paths and all HTTP methods
                    "/*/*": api_gateway.MethodDeploymentOptions(
                        throttling_rate_limit=100,
                        throttling_burst_limit=200
                    )
                })
            )