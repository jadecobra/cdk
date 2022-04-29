import aws_cdk
import constructs
import well_architected
import well_architected_api
import json


class ApiDynamodb(well_architected.WellArchitectedStack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        partition_key:str,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        self.error_topic = self.create_error_topic(id)
        rest_api = self.create_rest_api()
        api_gateway_service_role = self.create_api_gateway_service_role()

        dynamodb_table = self.create_dynamodb_table(partition_key)
        dynamodb_table.grant_read_write_data(api_gateway_service_role)
        self.add_method_to_rest_api(
            rest_api=rest_api,
            api_gateway_service_role=api_gateway_service_role,
            dynamodb_table_name=dynamodb_table.table_name,
            dynamodb_partition_key=partition_key
        )
        self.create_lambda_function_with_dynamodb_event_source(dynamodb_table)

    def create_error_topic(self, id):
        return aws_cdk.aws_sns.Topic(self, 'SnsTopic', display_name=id)

    def add_method_to_rest_api(
        self, rest_api=None, api_gateway_service_role=None,
        dynamodb_table_name=None, dynamodb_partition_key=None
    ):
        return rest_api.root.add_resource(
            'InsertItem'
        ).add_method(
            'POST',
            self.integrate_rest_api_with_dynamodb_put_item(
                api_gateway_service_role=api_gateway_service_role,
                dynamodb_table_name=dynamodb_table_name,
                dynamodb_partition_key=dynamodb_partition_key,
            ),
            method_responses=self.create_method_responses(
                rest_api=rest_api,
                dynamodb_partition_key=dynamodb_partition_key
            )
        )

    @staticmethod
    def create_api_request_template(template, separators=(',', ':')):
        return {
            'application/json': json.dumps(template, separators=separators)
            if not isinstance(template, aws_cdk.aws_apigateway.Model) else template
        }

    def success_response_template(self, partition_key=None):
        return self.create_api_request_template(
            template={partition_key: 'item added to db'},
            separators=None,
        )

    def error_response_template(self):
        return self.create_api_request_template({
            "state": 'error',
            "message": "$util.escapeJavaScript($input.path('$.errorMessage'))"
        })

    def request_template(self, table_name):
        return self.create_api_request_template({
            "TableName": table_name,
            "Item": {
                "message": { "S": "$input.path('$.message')" }
            }
        })

    def success_response_model(self, dynamodb_partition_key):
        return dict(
            model_name='ResponseModel',
            response_type='pollResponse',
            response_templates=self.success_response_template(dynamodb_partition_key),
        )

    def error_response_model(self):
        return dict(
            model_name='ErrorResponseModel',
            response_type='errorResponse',
            additional_properties='state',
            response_templates=self.error_response_template(),
            selection_pattern="^\[BadRequest\].*",
            response_parameters=self.create_response_parameters(
                content_type="'application/json'",
                origin="'*'",
                credentials="'true'",
            )
        )

    def get_response_status_mappings(self, dynamodb_partition_key):
        return {
            '200': self.success_response_model(dynamodb_partition_key),
            '400': self.error_response_model(),
        }

    def get_integration_responses(self, dynamodb_partition_key):
        return [
            aws_cdk.aws_apigateway.IntegrationResponse(
                status_code=status_code,
                response_templates=values['response_templates'],
                response_parameters=values.get('response_parameters'),
                selection_pattern=values.get('selection_pattern'),
            ) for status_code, values in self.get_response_status_mappings(dynamodb_partition_key).items()
        ]

    def create_api_integration_options(self, api_gateway_service_role=None, dynamodb_table_name=None, dynamodb_partition_key=None):
        return aws_cdk.aws_apigateway.IntegrationOptions(
            credentials_role=api_gateway_service_role,
            request_templates=self.request_template(dynamodb_table_name),
            passthrough_behavior=aws_cdk.aws_apigateway.PassthroughBehavior.NEVER,
            integration_responses=self.get_integration_responses(dynamodb_partition_key)
        )

    def integrate_rest_api_with_dynamodb_put_item(self, api_gateway_service_role=None, dynamodb_table_name=None, dynamodb_partition_key=None):
        return aws_cdk.aws_apigateway.Integration(
            type=aws_cdk.aws_apigateway.IntegrationType.AWS,
            integration_http_method='POST',
            uri='arn:aws:apigateway:us-east-1:dynamodb:action/PutItem',
            options=self.create_api_integration_options(
                api_gateway_service_role=api_gateway_service_role,
                dynamodb_table_name=dynamodb_table_name,
                dynamodb_partition_key=dynamodb_partition_key,
            )
        )

    @staticmethod
    def create_response_parameters(content_type=True, origin=True, credentials=True):
        return {
            'method.response.header.Content-Type': content_type,
            'method.response.header.Access-Control-Allow-Origin': origin,
            'method.response.header.Access-Control-Allow-Credentials': credentials,
        }

    @staticmethod
    def json_string():
        return aws_cdk.aws_apigateway.JsonSchema(
            type=aws_cdk.aws_apigateway.JsonSchemaType.STRING
        )

    def create_json_schema(self, dynamodb_partition_key=None, response_type=None, additional_properties=None):
        properties = [dynamodb_partition_key]
        properties.append(additional_properties) if additional_properties else None
        return aws_cdk.aws_apigateway.JsonSchema(
            schema=aws_cdk.aws_apigateway.JsonSchemaVersion.DRAFT4,
            title=response_type,
            type=aws_cdk.aws_apigateway.JsonSchemaType.OBJECT,
            properties={ key: self.json_string() for key in properties }
        )

    def create_response_models(self, rest_api=None, dynamodb_partition_key=None):
        return (
            (
                status_code,
                rest_api.add_model(
                    response['model_name'],
                    content_type='application/json',
                    model_name=response['model_name'],
                    schema=self.create_json_schema(
                        dynamodb_partition_key=dynamodb_partition_key,
                        response_type=response['response_type'],
                        additional_properties=response.get('additional_properties'),
                    )
                )
            ) for status_code, response
            in self.get_response_status_mappings(dynamodb_partition_key).items()
        )

    def create_method_responses(self, rest_api=None, dynamodb_partition_key=None):
        return [
            aws_cdk.aws_apigateway.MethodResponse(
                status_code=status_code,
                response_parameters=self.create_response_parameters(),
                response_models=self.create_api_request_template(response_model),
            ) for status_code, response_model in self.create_response_models(
                rest_api=rest_api,
                dynamodb_partition_key=dynamodb_partition_key,
            )
        ]

    def create_dynamodb_table(self, partition_key):
        return aws_cdk.aws_dynamodb.Table(
            self, "DynamoDbTable",
            stream=aws_cdk.aws_dynamodb.StreamViewType.NEW_IMAGE,
            partition_key=aws_cdk.aws_dynamodb.Attribute(
                name=partition_key,
                type=aws_cdk.aws_dynamodb.AttributeType.STRING,
            ),
        )

    def create_lambda_function_with_dynamodb_event_source(self, dynamodb_table):
        return aws_cdk.aws_lambda.Function(
            self, 'LambdaFunction',
            runtime=aws_cdk.aws_lambda.Runtime.PYTHON_3_8,
            handler="subscribe.handler",
            code=aws_cdk.aws_lambda.Code.from_asset("lambda_functions/subscribe")
        ).add_event_source(
            aws_cdk.aws_lambda_event_sources.DynamoEventSource(
                table=dynamodb_table,
                starting_position=aws_cdk.aws_lambda.StartingPosition.LATEST,
            )
        )

    def create_rest_api(self):
        return well_architected_api.WellArchitectedApi(
            self, 'RestApiGateway',
            error_topic=self.error_topic,
            api=aws_cdk.aws_apigateway.RestApi(
                self, 'ApiGateway',
                deploy_options=aws_cdk.aws_apigateway.StageOptions(
                    metrics_enabled=True,
                    logging_level=aws_cdk.aws_apigateway.MethodLoggingLevel.INFO,
                    data_trace_enabled=True,
                    stage_name='prod',
                )
            )
        ).api
        return aws_cdk.aws_apigateway.RestApi(
            self, 'ApiGateway',
            deploy_options=aws_cdk.aws_apigateway.StageOptions(
                metrics_enabled=True,
                logging_level=aws_cdk.aws_apigateway.MethodLoggingLevel.INFO,
                data_trace_enabled=True,
                stage_name='prod',
            )
        )

    def create_api_gateway_service_role(self):
        return aws_cdk.aws_iam.Role(
            self, 'ApiGatewayServiceRole',
            assumed_by=aws_cdk.aws_iam.ServicePrincipal('apigateway.amazonaws.com'),
        )