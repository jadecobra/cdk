from aws_cdk import (
    aws_apigateway as api_gw,
    aws_iam as iam,
    aws_sns as sns,
    core
)
import json

class TheXrayTracerStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ###
        # SNS Topic Creation
        # Our API Gateway posts messages directly to this
        ###
        topic = sns.Topic(self, 'TheXRayTracerSnsFanOutTopic', display_name='The XRay Tracer Fan Out Topic')
        self.sns_topic_arn = topic.topic_arn

        ###
        # API Gateway Creation
        # This is complicated because it is a direct SNS integration through VTL not a proxy integration
        # Tracing is enabled for X-Ray
        ###

        self.gateway = api_gw.RestApi(
            self, 'xrayTracerAPI',
            deploy_options=api_gw.StageOptions(
                metrics_enabled=True,
                logging_level=api_gw.MethodLoggingLevel.INFO,
                data_trace_enabled=True,
                tracing_enabled=True,
                stage_name='prod'
            )
        )

        # Give our gateway permissions to interact with SNS
        self.api_gw_sns_role = iam.Role(
            self, 'ApiGatewaySNSRole',
            assumed_by=iam.ServicePrincipal('apigateway.amazonaws.com')
        )
        topic.grant_publish(self.api_gw_sns_role)

        # shortening the lines of later code
        schema = api_gw.JsonSchema
        schema_type = api_gw.JsonSchemaType

        # Because this isn't a proxy integration, we need to define our response model
        self.response_model = self.gateway.add_model(
            'ResponseModel',
            content_type='application/json',
            model_name='ResponseModel',
            schema=schema(
                schema=api_gw.JsonSchemaVersion.DRAFT4,
                title='pollResponse',
                type=schema_type.OBJECT,
                properties={
                    'message': schema(type=schema_type.STRING)
                }
            )
        )

        self.error_response_model = self.gateway.add_model(
            'ErrorResponseModel',
            content_type='application/json',
            model_name='ErrorResponseModel',
            schema=schema(
                schema=api_gw.JsonSchemaVersion.DRAFT4,
                title='errorResponse',
                type=schema_type.OBJECT,
                properties={
                    'state': schema(type=schema_type.STRING),
                    'message': schema(type=schema_type.STRING)
                }
            )
        )

        self.request_template = "Action=Publish&" + \
            "TargetArn=$util.urlEncode('" + topic.topic_arn + "')&" + \
            "Message=$util.urlEncode($context.path)&" + \
            "Version=2010-03-31"

        # This is the VTL to transform the error response
        error_template = {
            "state": 'error',
            "message": "$util.escapeJavaScript($input.path('$.errorMessage'))"
        }
        self.error_template_string = json.dumps(error_template, separators=(',', ':'))

        self.create_root_endpoint()
        self.create_proxy_endpoint()

    def integration_options(self):
        # This is how our gateway chooses what response to send based on selection_pattern
        return api_gw.IntegrationOptions(
            credentials_role=self.api_gw_sns_role,
            request_parameters={
                'integration.request.header.Content-Type': "'application/x-www-form-urlencoded'"
            },
            request_templates=self.create_response_template(self.request_template),
            passthrough_behavior=api_gw.PassthroughBehavior.NEVER,
            integration_responses=[
                api_gw.IntegrationResponse(
                    status_code='200',
                    response_templates=self.create_response_template(
                        json.dumps({"message": 'message added to topic'})
                    ),
                ),
                api_gw.IntegrationResponse(
                    selection_pattern="^\[Error\].*",
                    status_code='400',
                    response_templates=self.create_response_template(self.error_template_string),
                    response_parameters=self.integration_response_parameters()
                )
            ]
        )

    @staticmethod
    def create_response_template(model):
        return {'application/json': model}

    @staticmethod
    def create_response_parameters(content_type=True, origin=True, credentials=True):
        return {
            'method.response.header.Content-Type': content_type,
            'method.response.header.Access-Control-Allow-Origin': origin,
            'method.response.header.Access-Control-Allow-Credentials': credentials
        }

    def integration_response_parameters(self):
        return self.create_response_parameters(
            content_type="'application/json'",
            origin="'*'",
            credentials="'true'"
        )

    def create_method_response(self, status_code='200', response_model=None):
        return api_gw.MethodResponse(
            status_code=status_code,
            response_parameters=self.create_response_parameters(),
            response_models=self.create_response_template(response_model)
        )

    def method_responses(self):
        return [
            self.create_method_response(response_model=self.response_model),
            self.create_method_response(status_code='400', response_model=self.error_response_model),
        ]

    def create_endpoint(self, resource):
        return resource.add_method(
            'GET', api_gw.Integration(
                type=api_gw.IntegrationType.AWS,
                integration_http_method='POST',
                uri=f'arn:aws:apigateway:{self.region}:sns:path//',
                options=self.integration_options()
            ),
            method_responses=self.method_responses()
        )

    def create_root_endpoint(self):
        return self.create_endpoint(self.gateway.root)

    def create_proxy_endpoint(self):
        return self.create_endpoint(
            self.gateway.root.add_resource('{proxy+}')
        )