import aws_cdk
import constructs
import well_architected
import well_architected_api

class ALambdaRestAPIGatewayConstruct(well_architected.WellArchitectedConstruct):

    def __init__(self, scope: constructs.Construct, id: str, lambda_function: aws_cdk.aws_lambda.Function, error_topic:aws_cdk.aws_sns.Topic=None, **kwargs) -> None:
        super().__init__(
            scope, id,
            error_topic=error_topic,
            **kwargs
        )

        self.rest_api = self.create_rest_api()
        self.error_topic = error_topic
        self.api_id = self.rest_api.rest_api_id
        self.create_api_method(
            resource=self.create_api_resource(self.rest_api),
            lambda_function=lambda_function,
        )

        # fix resource_arn
        # self.resource_arn = f"arn:aws:apigateway:{self.region}::/restapis/{self.api_id}/stages/{self.rest_api.deployment_stage.stage_name}"
        self.resource_arn = "arn:aws:apigateway:{self.region}::/restapis/{self.api_id}/stages/{self.rest_api.deployment_stage.stage_name}"

        well_architected_api.WellArchitectedApi(
            self, 'ApiGatewayCloudWatch',
            api=self.rest_api,
            # api_id=self.api_id,
            error_topic=self.error_topic,
        )

    def method_origin(self):
        return 'method.response.header.Access-Control-Allow-Origin'

    def status_code(self):
        return '200'

    def create_method_responses(self):
        return [
            aws_cdk.aws_apigateway.MethodResponse(
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
            aws_cdk.aws_apigateway.IntegrationResponse(
                status_code=self.status_code(),
                response_parameters={
                    self.method_origin(): "'*'"
                }
            )
        ]

    def create_lambda_integration(self, lambda_function):
        return aws_cdk.aws_apigateway.LambdaIntegration(
            lambda_function,
            proxy=False,
            integration_responses=self.create_integration_responses()
        )

    def create_api_resource(self, api):
        return api.root.add_resource('hello')

    def create_log_group(self):
        return aws_cdk.aws_logs.LogGroup(self, "helloAPILogs")

    def method_deployment_options(self):
        return {
            # This special path applies to all resource paths and all HTTP methods
            "/*/*": aws_cdk.aws_apigateway.MethodDeploymentOptions(
                throttling_rate_limit=100,
                throttling_burst_limit=200
            )
        }

    def deploy_options(self):
        return aws_cdk.aws_apigateway.StageOptions(
            method_options=self.method_deployment_options(),
            access_log_format=aws_cdk.aws_apigateway.AccessLogFormat.clf(),
            access_log_destination=aws_cdk.aws_apigateway.LogGroupLogDestination(
                self.create_log_group()
            ),
        )

    def create_rest_api(self):
        return aws_cdk.aws_apigateway.RestApi(
            self, 'LambdaAPIGateway',
            rest_api_name='hello',
            endpoint_types=[aws_cdk.aws_apigateway.EndpointType.REGIONAL],
            deploy_options=self.deploy_options(),
        )


class LambdaRestAPIGatewayConstruct(well_architected.WellArchitectedConstruct):

    def __init__(self, scope: constructs.Construct, id: str, lambda_function: aws_cdk.aws_lambda.Function, error_topic:aws_cdk.aws_sns.Topic=None, **kwargs) -> None:
        super().__init__(
            scope, id,
            error_topic=error_topic,
            **kwargs
        )

        self.rest_api = self.create_rest_api()
        self.error_topic = error_topic
        self.api_id = self.rest_api.rest_api_id
        self.create_api_method(
            resource=self.create_api_resource(self.rest_api),
            lambda_function=lambda_function,
        )

        # fix resource_arn
        # self.resource_arn = f"arn:aws:apigateway:{self.region}::/restapis/{self.api_id}/stages/{self.rest_api.deployment_stage.stage_name}"
        self.resource_arn = "arn:aws:apigateway:{self.region}::/restapis/{self.api_id}/stages/{self.rest_api.deployment_stage.stage_name}"

        well_architected_api.WellArchitectedApi(
            self, 'ApiGatewayCloudWatch',
            api=self.rest_api,
            # api_id=self.api_id,
            error_topic=self.error_topic,
        )

    def method_origin(self):
        return 'method.response.header.Access-Control-Allow-Origin'

    def status_code(self):
        return '200'

    def create_method_responses(self):
        return [
            aws_cdk.aws_apigateway.MethodResponse(
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
            aws_cdk.aws_apigateway.IntegrationResponse(
                status_code=self.status_code(),
                response_parameters={
                    self.method_origin(): "'*'"
                }
            )
        ]

    def create_lambda_integration(self, lambda_function):
        return aws_cdk.aws_apigateway.LambdaIntegration(
            lambda_function,
            proxy=False,
            integration_responses=self.create_integration_responses()
        )

    def create_api_resource(self, api):
        return api.root.add_resource('hello')

    def create_log_group(self):
        return aws_cdk.aws_logs.LogGroup(self, "helloAPILogs")

    def method_deployment_options(self):
        return {
            # This special path applies to all resource paths and all HTTP methods
            "/*/*": aws_cdk.aws_apigateway.MethodDeploymentOptions(
                throttling_rate_limit=100,
                throttling_burst_limit=200
            )
        }

    def deploy_options(self):
        return aws_cdk.aws_apigateway.StageOptions(
            method_options=self.method_deployment_options(),
            access_log_format=aws_cdk.aws_apigateway.AccessLogFormat.clf(),
            access_log_destination=aws_cdk.aws_apigateway.LogGroupLogDestination(
                self.create_log_group()
            ),
        )

    def create_rest_api(self):
        return aws_cdk.aws_apigateway.RestApi(
            self, 'LambdaAPIGateway',
            rest_api_name='hello',
            endpoint_types=[aws_cdk.aws_apigateway.EndpointType.REGIONAL],
            deploy_options=self.deploy_options(),
        )

class LambdaRestAPIGatewayStack(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, id: str, lambda_function: aws_cdk.aws_lambda.Function, error_topic:aws_cdk.aws_sns.Topic=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.rest_api = LambdaRestAPIGatewayConstruct(
            self, id,
            lambda_function=lambda_function,
            error_topic=error_topic,
            **kwargs
        )