import jadecobra.toolkit
import src.well_architected_constructs

from  tests.test_well_architected_constructs import TestWellArchitectedConstructAttributes


class TestApiConstructAttributes(TestWellArchitectedConstructAttributes):

    def test_api(self):
        self.assert_attributes_equal(
            src.well_architected_constructs.api.Api,
            [
                *self.well_architected_construct_attributes(),
                'add_api_gateway_metric',
                'create_api_gateway_4xx_alarm',
                'create_api_gateway_5xx_alarm',
                'create_api_gateway_errors_widget',
                'create_api_gateway_latency_alarm',
                'create_api_gateway_latency_widget',
                'create_api_gateway_number_of_requests_widget',
                'create_api_gateway_service_role',
                'get_api_id',
                'metric_names',
                'percentile_statistics',
            ]
        )

    def test_api_lambda_dynamodb(self):
        self.assert_attributes_equal(
            src.well_architected_constructs.api_lambda_dynamodb.ApiLambdaDynamodbConstruct,
            [
                *self.well_architected_construct_attributes(),
                'create_api',
                'create_http_api_lambda',
                'create_rest_api_lambda',
            ]
        )

    def test_http_api_step_functions(self):
        self.assert_attributes_equal(
            src.well_architected_constructs.http_api_step_functions.HttpApiStepFunctionsConstruct,
            [
                *self.well_architected_construct_attributes(),
                'add_api_gateway_metric',
                'create_api_gateway_4xx_alarm',
                'create_api_gateway_5xx_alarm',
                'create_api_gateway_errors_widget',
                'create_api_gateway_latency_alarm',
                'create_api_gateway_latency_widget',
                'create_api_gateway_number_of_requests_widget',
                'create_api_gateway_service_role',
                'create_http_api_step_functions_route',
                'create_http_api_stepfunctions_integration',
                'get_api_id',
                'metric_names',
                'percentile_statistics',
            ]
        )

    def test_rest_api(self):
        self.assert_attributes_equal(
            src.well_architected_constructs.rest_api.RestApiConstruct,
            [
                *self.well_architected_construct_attributes(),
                'add_api_gateway_metric',
                'add_method',
                'create_api_gateway_4xx_alarm',
                'create_api_gateway_5xx_alarm',
                'create_api_gateway_errors_widget',
                'create_api_gateway_latency_alarm',
                'create_api_gateway_latency_widget',
                'create_api_gateway_number_of_requests_widget',
                'create_api_gateway_service_role',
                'create_api_integration',
                'create_integration_response',
                'create_json_template',
                'create_method_response',
                'create_method_responses',
                'create_response_model',
                'create_response_parameters',
                'create_schema',
                'error_response',
                'get_api_id',
                'get_integration_options',
                'get_integration_responses',
                'get_stage_options',
                'json_content_type',
                'metric_names',
                'percentile_statistics',
                'string_schema_type',
                'success_response',
            ]
        )

    def test_rest_api_sns(self):
        self.assert_attributes_equal(
            src.well_architected_constructs.rest_api_sns.RestApiSnsConstruct,
            [
                *self.well_architected_construct_attributes(),
                'add_api_gateway_metric',
                'add_method',
                'call_sns_publish_api',
                'create_api_gateway_4xx_alarm',
                'create_api_gateway_5xx_alarm',
                'create_api_gateway_errors_widget',
                'create_api_gateway_latency_alarm',
                'create_api_gateway_latency_widget',
                'create_api_gateway_number_of_requests_widget',
                'create_api_gateway_service_role',
                'create_api_integration',
                'create_integration_response',
                'create_json_template',
                'create_method_response',
                'create_method_responses',
                'create_response_model',
                'create_response_parameters',
                'create_schema',
                'error_response',
                'get_api_id',
                'get_integration_options',
                'get_integration_responses',
                'get_stage_options',
                'json_content_type',
                'metric_names',
                'parse_additional_parameters',
                'percentile_statistics',
                'string_schema_type',
                'success_response',
            ]
        )
