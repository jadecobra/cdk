import aws_cdk
import constructs
import json


class SnsRestApi(aws_cdk.Stack):
    def __init__(self, scope: constructs.Construct, id: str, sns_topic: aws_cdk.aws_sns.ITopic = None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.sns_topic = sns_topic
        self.gateway = self.create_rest_api()
        self.api_gateway_sns_role = self.create_iam_role()
        self.sns_topic.grant_publish(self.api_gateway_sns_role)

        # Because this isn't a proxy integration, we need to define our response model
        self.response_model = self.create_response_model(
            model_name='ResponseModel',
            schema=self.create_schema(
                title='pollResponse',
                properties=self.response_properties()
            )
        )

        self.error_response_model = self.create_response_model(
            model_name='ErrorResponseModel',
            schema=self.create_schema(
                title='errorResponse',
                properties={
                    **self.response_properties(),
                    'state': self.json_schema_string(),
                }
            )
        )

        self.create_root_endpoint()
        self.create_proxy_endpoint()

    def create_rest_api(self):
        return aws_cdk.aws_apigateway.RestApi(
            self, 'RestApi',
            deploy_options=aws_cdk.aws_apigateway.StageOptions(
                metrics_enabled=True,
                logging_level=aws_cdk.aws_apigateway.MethodLoggingLevel.INFO,
                data_trace_enabled=True,
                tracing_enabled=True,
                stage_name='prod'
            )
        )

    def create_iam_role(self):
        return aws_cdk.aws_iam.Role(
            self, 'ApiGatewaySNSRole',
            assumed_by=aws_cdk.aws_iam.ServicePrincipal('apigateway.amazonaws.com')
        )

    def response_properties(self):
        return {'message': self.json_schema_string()}

    @staticmethod
    def json_schema_string():
        return aws_cdk.aws_apigateway.JsonSchema(
            type=aws_cdk.aws_apigateway.JsonSchemaType.STRING
        )

    def create_response_model(self, model_name=None, schema=None):
        return self.gateway.add_model(
            model_name,
            content_type='application/json',
            model_name=model_name,
            schema=schema
        )

    @staticmethod
    def create_schema(title=None, properties=None):
        return aws_cdk.aws_apigateway.JsonSchema(
            schema=aws_cdk.aws_apigateway.JsonSchemaVersion.DRAFT4,
            title=title,
            type=aws_cdk.aws_apigateway.JsonSchemaType.OBJECT,
            properties=properties,
        )

    def request_template(self):
        return (
            f"Action=Publish&TargetArn=$util.urlEncode('{self.sns_topic.topic_arn}')"
            "&Message=$util.urlEncode($context.path)&Version=2010-03-31"
        )

    @staticmethod
    def error_template():
        return json.dumps(
            {
                "state": 'error',
                "message": "$util.escapeJavaScript($input.path('$.errorMessage'))"
            },
            separators=(',', ':')
        )

    @staticmethod
    def response_template():
        return json.dumps({"message": 'message added to topic'})

    @staticmethod
    def create_response_template(model):
        return {'application/json': model}

    def integration_options(self):
        # This is how our gateway chooses what response to send based on selection_pattern
        return aws_cdk.aws_apigateway.IntegrationOptions(
            credentials_role=self.api_gateway_sns_role,
            request_parameters={
                'integration.request.header.Content-Type': "'application/x-www-form-urlencoded'"
            },
            request_templates=self.create_response_template(self.request_template()),
            passthrough_behavior=aws_cdk.aws_apigateway.PassthroughBehavior.NEVER,
            integration_responses=[
                aws_cdk.aws_apigateway.IntegrationResponse(
                    status_code='200',
                    response_templates=self.create_response_template(self.response_template()),
                ),
                aws_cdk.aws_apigateway.IntegrationResponse(
                    selection_pattern="^\[Error\].*",
                    status_code='400',
                    response_templates=self.create_response_template(self.error_template()),
                    response_parameters=self.integration_response_parameters()
                )
            ]
        )

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
        return aws_cdk.aws_apigateway.MethodResponse(
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
            'GET', aws_cdk.aws_apigateway.Integration(
                type=aws_cdk.aws_apigateway.IntegrationType.AWS,
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