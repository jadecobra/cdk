import aws_cdk
import constructs
import json
import well_architected
import well_architected.constructs.api as api


class RestApiConstruct(api.WellArchitectedApi):

    def __init__(
        self, scope: constructs.Construct, id: str,
        error_topic=None, api=None, **kwargs,
    ):
        super().__init__(
            scope, id,
            error_topic=error_topic,
            api=api,
            **kwargs,
        )
        self.api_gateway_service_role = self.create_api_gateway_service_role()

    def create_api_gateway_service_role(self):
        return aws_cdk.aws_iam.Role(
            self, 'ApiGatewayServiceRole',
            assumed_by=aws_cdk.aws_iam.ServicePrincipal('apigateway.amazonaws.com'),
        )

    @staticmethod
    def create_response_parameters(content_type=True, allow_origin=True, allow_credentials=True):
        return {
            'method.response.header.Content-Type': content_type,
            'method.response.header.Access-Control-Allow-Origin': allow_origin,
            'method.response.header.Access-Control-Allow-Credentials': allow_credentials,
        }

    @staticmethod
    def content_type():
        return 'application/json'

    def create_json_template(self, template):
        return {self.content_type(): template}

    def create_method_response(self, status_code=None, response_model=None):
        return aws_cdk.aws_apigateway.MethodResponse(
            status_code=str(status_code),
            response_parameters=self.create_response_parameters(),
            response_models=self.create_json_template(response_model)
        )

    @staticmethod
    def create_schema(title=None, properties=None):
        return aws_cdk.aws_apigateway.JsonSchema(
            schema=aws_cdk.aws_apigateway.JsonSchemaVersion.DRAFT4,
            title=title,
            type=aws_cdk.aws_apigateway.JsonSchemaType.OBJECT,
            properties=properties
        )

    @staticmethod
    def string_schema_type():
        return aws_cdk.aws_apigateway.JsonSchema(
            type=aws_cdk.aws_apigateway.JsonSchemaType.STRING
        )


    def create_response_model(
        self, rest_api=None, model_name=None, properties=None
    ):
        property_keys = ['message']
        property_keys.append(properties) if properties else None
        return rest_api.add_model(
            model_name,
            content_type=self.content_type(),
            model_name=model_name,
            schema=self.create_schema(
                title=model_name,
                properties={key: self.string_schema_type() for key in property_keys},
            )
        )

    def success_response(self, rest_api):
        return (
            200,
            self.create_response_model(
                rest_api=rest_api,
                model_name='pollResponse',
            )
        )

    def error_response(self, rest_api):
        return (
            400,
            self.create_response_model(
                rest_api=rest_api,
                model_name='errorResponse',
                properties='state',
            )
        )

    def create_method_responses(self, rest_api):
        return [
            self.create_method_response(
                status_code=status_code,
                response_model=response_model
            ) for status_code, response_model
            in (
                self.success_response(rest_api),
                self.error_response(rest_api),
            )
        ]

    def add_method(
        self, integration=None,
        method='POST', path=None
    ):
        return self.api.root.add_resource(
            path
        ).add_method(
            method,
            integration,
            method_responses=self.create_method_responses(self.api)
        )


class RestApiLambdaStack(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, id: str, lambda_function: aws_cdk.aws_lambda.Function, error_topic:aws_cdk.aws_sns.Topic=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.rest_api = LambdaRestAPIGatewayConstruct(
            self, id,
            lambda_function=lambda_function,
            error_topic=error_topic,
            **kwargs
        )