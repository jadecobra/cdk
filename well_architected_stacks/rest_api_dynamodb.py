import aws_cdk
import aws_cdk.aws_apigatewayv2_alpha
import constructs
import well_architected
import well_architected_constructs.dynamodb_table
import well_architected_constructs.lambda_function
import well_architected_constructs.rest_api_sns
import json


class RestApiDynamodb(well_architected.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        partition_key:str,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        rest_api = self.create_rest_api(self.error_topic)
        dynamodb_table = self.create_dynamodb_table(
            partition_key=partition_key,
            error_topic=self.error_topic,
        )
        dynamodb_table.grant_read_write_data(rest_api.api_gateway_service_role)
        rest_api.add_method(
            method='POST',
            path='InsertItem',
            integration=rest_api.create_api_integration(
                uri='arn:aws:apigateway:us-east-1:dynamodb:action/PutItem',
                request_templates=self.get_request_template(dynamodb_table.table_name),
                success_response_templates=self.success_response_template(partition_key, rest_api=rest_api),
                error_response_templates=self.error_response_template(rest_api),
                error_selection_pattern="^\[BadRequest\].*",
            )
        )
        self.create_lambda_function_with_dynamodb_event_source(
            dynamodb_table=dynamodb_table,
            error_topic=self.error_topic,
        )

    @staticmethod
    def create_json_template(template, separators=(',', ':')):
        return {
            'application/json': json.dumps(template, separators=separators)
            if not isinstance(template, aws_cdk.aws_apigateway.Model) else template
        }

    def success_response_template(self, partition_key=None, rest_api=None):
        return {partition_key: 'item added to db'}

    def error_response_template(self, rest_api):
        return {
            "state": 'error',
            "message": "$util.escapeJavaScript($input.path('$.errorMessage'))"
        }

    def get_request_template(self, table_name):
        return self.create_json_template({
            "TableName": table_name,
            "Item": {
                "message": { "S": "$input.path('$.message')" }
            }
        })

    # def success_response_model(self, dynamodb_partition_key):
    #     return dict(
    #         model_name='pollResponse',
    #         response_type='pollResponse',
    #         response_templates=self.success_response_template(dynamodb_partition_key),
    #     )

    @staticmethod
    def create_response_parameters(content_type=True, allow_origin=True, allow_credentials=True):
        return {
            'method.response.header.Content-Type': content_type,
            'method.response.header.Access-Control-Allow-Origin': allow_origin,
            'method.response.header.Access-Control-Allow-Credentials': allow_credentials,
        }

    def error_response_model(self):
        return dict(
            model_name='errorResponse',
            response_type='errorResponse',
            additional_properties='state',
            response_templates=self.error_response_template(),
            selection_pattern="^\[BadRequest\].*",
            response_parameters=self.create_response_parameters(
                content_type="'application/json'",
                allow_origin="'*'",
                allow_credentials="'true'",
            )
        )

    # def get_response_status_mappings(self, dynamodb_partition_key):
    #     return {
    #         '200': self.success_response_model(dynamodb_partition_key),
    #         '400': self.error_response_model(),
    #     }

    # def get_integration_responses(self, dynamodb_partition_key):
    #     return [
    #         aws_cdk.aws_apigateway.IntegrationResponse(
    #             status_code=status_code,
    #             response_templates=values['response_templates'],
    #             response_parameters=values.get('response_parameters'),
    #             selection_pattern=values.get('selection_pattern'),
    #         ) for status_code, values in {
    #             '200': dict(
    #                 model_name='pollResponse',
    #                 response_templates=self.success_response_template(dynamodb_partition_key),
    #             ),
    #             '400': dict(
    #                 model_name='errorResponse',
    #                 additional_properties='state',
    #                 response_templates=self.error_response_template(),
    #                 selection_pattern="^\[BadRequest\].*",
    #                 response_parameters=self.create_response_parameters(
    #                     content_type="'application/json'",
    #                     allow_origin="'*'",
    #                     allow_credentials="'true'",
    #                 )
    #             ),
    #         }.items()
    #     ]

    @staticmethod
    def json_string():
        return aws_cdk.aws_apigateway.JsonSchema(
            type=aws_cdk.aws_apigateway.JsonSchemaType.STRING
        )

    def create_json_schema(
        self, dynamodb_partition_key=None, response_type=None,
        additional_properties=None
    ):
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

    def create_dynamodb_table(self, partition_key=None, error_topic=None):
        return well_architected_constructs.dynamodb_table.DynamoDBTableConstruct(
            self, 'DynamoDbTable',
            stream=aws_cdk.aws_dynamodb.StreamViewType.NEW_IMAGE,
            error_topic=error_topic,
            partition_key=partition_key,
        ).dynamodb_table

    def create_lambda_function_with_dynamodb_event_source(self, dynamodb_table=None, error_topic=None):
        return well_architected_constructs.lambda_function.LambdaFunctionConstruct(
            self, 'LambdaFunction',
            error_topic=error_topic,
            function_name='subscribe',
        ).lambda_function.add_event_source(
            aws_cdk.aws_lambda_event_sources.DynamoEventSource(
                table=dynamodb_table,
                starting_position=aws_cdk.aws_lambda.StartingPosition.LATEST,
            )
        )

    def create_rest_api(self, error_topic):
        return well_architected_constructs.rest_api_sns.RestApiConstruct(
            self, 'ApiGateway',
            error_topic=error_topic,
            api=aws_cdk.aws_apigateway.RestApi(
                self, 'RestApiDynamodb',
                deploy_options=aws_cdk.aws_apigateway.StageOptions(
                    metrics_enabled=True,
                    logging_level=aws_cdk.aws_apigateway.MethodLoggingLevel.INFO,
                    data_trace_enabled=True,
                    stage_name='prod',
                )
            )
        )