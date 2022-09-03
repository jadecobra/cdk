import jadecobra.toolkit
import src.well_architected_constructs as well_architected_constructs
import os


class TestWellArchitectedConstructs(jadecobra.toolkit.TestCase):

    def test_well_architected_constructs_files(self):
        self.assertEqual(
            sorted(os.listdir('src/well_architected_constructs')),
            [
                '__init__.py',
                '__pycache__',
                'api.py',
                'api_lambda.py',
                'api_lambda_dynamodb.py',
                'dynamodb_table.py',
                'http_api_step_functions.py',
                'lambda_function.py',
                'rest_api.py',
                'rest_api_sns.py',
                'sns_lambda.py',
                'web_application_firewall.py',
                'well_architected_construct.py',
            ]
        )

    def test_well_architected_constructs_attributes(self):
        self.assert_attributes_equal(
            well_architected_constructs,
            [
                '__builtins__',
                '__cached__',
                '__doc__',
                '__file__',
                '__loader__',
                '__name__',
                '__package__',
                '__path__',
                '__spec__',
                'api',
                'api_lambda',
                'api_lambda_dynamodb',
                'dynamodb_table',
                'http_api_step_functions',
                'lambda_function',
                'rest_api',
                'rest_api_sns',
                'sns_lambda',
                'web_application_firewall',
                'well_architected_construct',
            ]
        )

    @staticmethod
    def cloudwatch_attributes():
        return (
            'cloudwatch_math_sum',
            'create_cloudwatch_alarm',
            'create_cloudwatch_dashboard',
            'create_cloudwatch_math_expression',
            'create_cloudwatch_widget',
            'create_sns_topic',
        )

    def default_attributes(self):
        return (
            '__class__',
            '__delattr__',
            '__dict__',
            '__dir__',
            '__doc__',
            '__eq__',
            '__format__',
            '__ge__',
            '__getattribute__',
            '__gt__',
            '__hash__',
            '__init__',
            '__init_subclass__',
            '__jsii_declared_type__',
            '__jsii_ifaces__',
            '__jsii_type__',
            '__le__',
            '__lt__',
            '__module__',
            '__ne__',
            '__new__',
            '__reduce__',
            '__reduce_ex__',
            '__repr__',
            '__setattr__',
            '__sizeof__',
            '__str__',
            '__subclasshook__',
            '__weakref__',
            *self.cloudwatch_attributes(),
        )

    def test_api(self):
        self.assert_attributes_equal(
            well_architected_constructs.api.Api,
            sorted([
                *self.default_attributes(),
                'add_api_gateway_metric',
                'create_api_gateway_4xx_alarm',
                'create_api_gateway_5xx_alarm',
                'create_api_gateway_errors_widget',
                'create_api_gateway_latency_alarm',
                'create_api_gateway_latency_widget',
                'create_api_gateway_number_of_requests_widget',
                'create_api_gateway_service_role',
                # 'create_cloudwatch_alarm',
                # 'create_cloudwatch_dashboard',
                # 'create_cloudwatch_math_expression',
                # 'create_cloudwatch_widget',
                'create_cloudwatch_widgets',
                # 'create_sns_topic',
                'get_api_id',
                'is_construct',
                'metric_names',
                'node',
                'percentile_statistics',
                'to_string'
            ])
        )

    # def test_api_lambda_dynamodb(self):
    #     self.assert_attributes_equal(
    #         well_architected_constructs.api_lambda_dynamodb.ApiLambdaDynamodbConstruct,
    #         sorted([
    #             *self.default_attributes(),
    #             *self.cloudwatch_attributes(),
    #             # 'create_cloudwatch_alarm',
    #             # 'create_cloudwatch_dashboard',
    #             # 'create_cloudwatch_math_expression',
    #             # 'create_cloudwatch_widget',
    #             'create_dynamodb_table',
    #             'create_lambda_function',
    #             'create_sns_topic',
    #             'is_construct',
    #             'node',
    #             'to_string'
    #         ])
    #     )

    # def test_dynamodb_table(self):
    #     self.assert_attributes_equal(
    #         well_architected_constructs.dynamodb_table.DynamodbTableConstruct,
    #         sorted([
    #             *self.default_attributes(),
    #             *self.cloudwatch_attributes(),
    #             # 'create_cloudwatch_alarm',
    #             # 'create_cloudwatch_dashboard',
    #             # 'create_cloudwatch_math_expression',
    #             # 'create_cloudwatch_widget',
    #             'create_cloudwatch_widgets',
    #             'create_latency_widget',
    #             'create_read_write_capacity_widget',
    #             'create_sns_topic',
    #             'create_system_errors_alarm',
    #             'create_throttles_alarm',
    #             'create_throttles_metric',
    #             'create_throttles_widget',
    #             'create_user_errors_alarm',
    #             'get_dynamodb_key',
    #             'get_dynamodb_metric',
    #             'is_construct',
    #             'node',
    #             'to_string'
    #         ])
    #     )

    # def test_http_api_step_functions(self):
    #     self.assert_attributes_equal(
    #         well_architected_constructs.http_api_step_functions.HttpApiStepFunctionsConstruct,
    #         sorted([
    #             *self.default_attributes(),
    #             'add_api_gateway_metric',
    #             *self.cloudwatch_attributes(),
    #             'create_api_gateway_4xx_alarm',
    #             'create_api_gateway_5xx_alarm',
    #             'create_api_gateway_errors_widget',
    #             'create_api_gateway_latency_alarm',
    #             'create_api_gateway_latency_widget',
    #             'create_api_gateway_number_of_requests_widget',
    #             'create_api_gateway_service_role',
    #             # 'create_cloudwatch_alarm',
    #             # 'create_cloudwatch_dashboard',
    #             # 'create_cloudwatch_math_expression',
    #             # 'create_cloudwatch_widget',
    #             'create_cloudwatch_widgets',
    #             'create_http_api_step_functions_route',
    #             'create_http_api_stepfunctions_integration',
    #             'create_sns_topic',
    #             'get_api_id',
    #             'is_construct',
    #             'metric_names',
    #             'node',
    #             'percentile_statistics',
    #             'to_string'
    #         ])
    #     )

    # def test_lambda_function(self):
    #     self.assert_attributes_equal(
    #         well_architected_constructs.lambda_function.LambdaFunctionConstruct,
    #         sorted([
    #             *self.default_attributes(),
    #             'add_event_bridge_rule',
    #             *self.cloudwatch_attributes(),
    #             # 'create_cloudwatch_alarm',
    #             # 'create_cloudwatch_dashboard',
    #             # 'create_cloudwatch_math_expression',
    #             # 'create_cloudwatch_widget',
    #             'create_cloudwatch_widgets',
    #             'create_invocation_longer_than_1_second_alarm',
    #             'create_invocations_error_greater_than_2_percent_alarm',
    #             'create_lambda_duration_widget',
    #             'create_lambda_error_percentage_metric',
    #             'create_lambda_error_percentage_widget',
    #             'create_lambda_throttled_percentage_metric',
    #             'create_lambda_throttled_percentage_widget',
    #             'create_layer',
    #             'create_layers',
    #             'create_sns_topic',
    #             'create_throttled_invocations_greater_than_2_percent_alarm',
    #             'get_lambda_function_metric',
    #             'is_construct',
    #             'node',
    #             'to_camel_case',
    #             'to_string'
    #         ])
    #     )

    # def test_rest_api(self):
    #     self.assert_attributes_equal(
    #         well_architected_constructs.rest_api.RestApiConstruct,
    #         sorted([
    #             *self.default_attributes(),
    #             'add_api_gateway_metric',
    #             'add_method',
    #             *self.cloudwatch_attributes(),
    #             'create_api_gateway_4xx_alarm',
    #             'create_api_gateway_5xx_alarm',
    #             'create_api_gateway_errors_widget',
    #             'create_api_gateway_latency_alarm',
    #             'create_api_gateway_latency_widget',
    #             'create_api_gateway_number_of_requests_widget',
    #             'create_api_gateway_service_role',
    #             'create_api_integration',
    #             # 'create_cloudwatch_alarm',
    #             # 'create_cloudwatch_dashboard',
    #             # 'create_cloudwatch_math_expression',
    #             # 'create_cloudwatch_widget',
    #             'create_cloudwatch_widgets',
    #             'create_integration_response',
    #             'create_json_template',
    #             'create_method_response',
    #             'create_method_responses',
    #             'create_response_model',
    #             'create_response_parameters',
    #             'create_schema',
    #             'create_sns_topic',
    #             'error_response',
    #             'get_api_id',
    #             'get_integration_options',
    #             'get_integration_responses',
    #             'get_stage_options',
    #             'is_construct',
    #             'json_content_type',
    #             'metric_names',
    #             'node',
    #             'percentile_statistics',
    #             'string_schema_type',
    #             'success_response',
    #             'to_string'
    #         ])
    #     )

    # def test_rest_api_sns(self):
    #     self.assert_attributes_equal(
    #         well_architected_constructs.rest_api_sns.RestApiSnsConstruct,
    #         sorted([
    #             *self.default_attributes(),
    #             'add_api_gateway_metric',
    #             'add_method',
    #             'call_sns_publish_api',
    #             *self.cloudwatch_attributes(),
    #             'create_api_gateway_4xx_alarm',
    #             'create_api_gateway_5xx_alarm',
    #             'create_api_gateway_errors_widget',
    #             'create_api_gateway_latency_alarm',
    #             'create_api_gateway_latency_widget',
    #             'create_api_gateway_number_of_requests_widget',
    #             'create_api_gateway_service_role',
    #             'create_api_integration',
    #             # 'create_cloudwatch_alarm',
    #             # 'create_cloudwatch_dashboard',
    #             # 'create_cloudwatch_math_expression',
    #             # 'create_cloudwatch_widget',
    #             'create_cloudwatch_widgets',
    #             'create_integration_response',
    #             'create_json_template',
    #             'create_method_response',
    #             'create_method_responses',
    #             'create_response_model',
    #             'create_response_parameters',
    #             'create_schema',
    #             'create_sns_topic',
    #             'error_response',
    #             'get_api_id',
    #             'get_integration_options',
    #             'get_integration_responses',
    #             'get_stage_options',
    #             'is_construct',
    #             'json_content_type',
    #             'metric_names',
    #             'node',
    #             'parse_additional_parameters',
    #             'percentile_statistics',
    #             'string_schema_type',
    #             'success_response',
    #             'to_string'
    #         ])
    #     )

    # def test_sns_lambda(self):
    #     self.assert_attributes_equal(
    #         well_architected_constructs.sns_lambda.SnsLambdaConstruct,
    #         sorted([
    #             *self.default_attributes(),
    #             *self.cloudwatch_attributes(),
    #             # 'create_cloudwatch_alarm',
    #             # 'create_cloudwatch_dashboard',
    #             # 'create_cloudwatch_math_expression',
    #             # 'create_cloudwatch_widget',
    #             'create_sns_topic',
    #             'is_construct',
    #             'node',
    #             'to_string'
    #         ])
    #     )

    # def test_web_application_firewall(self):
    #     self.assert_attributes_equal(
    #         well_architected_constructs.web_application_firewall.WebApplicationFirewall,
    #         sorted([
    #             *self.default_attributes(),
    #             'add_geoblock_rule',
    #             'anonymous_ip_rule',
    #             *self.cloudwatch_attributes(),
    #             'common_ruleset',
    #             'country_codes',
    #             # 'create_cloudwatch_alarm',
    #             # 'create_cloudwatch_dashboard',
    #             # 'create_cloudwatch_math_expression',
    #             # 'create_cloudwatch_widget',
    #             'create_managed_rule',
    #             'create_managed_rule_group_statement',
    #             'create_sns_topic',
    #             'create_visibility_configuration',
    #             'create_web_application_firewall',
    #             'create_web_application_firewall_association',
    #             'is_construct',
    #             'node',
    #             'restricted_ip_list_rule',
    #             'to_string',
    #             'web_application_firewall_rules'
    #         ])
    #     )

    # def test_well_architected_construct(self):
    #     self.assert_attributes_equal(
    #         well_architected_constructs.well_architected_construct.Construct,
    #         sorted([
    #             *self.default_attributes(),
    #             *self.cloudwatch_attributes(),
    #             # 'create_cloudwatch_alarm',
    #             # 'create_cloudwatch_dashboard',
    #             # 'create_cloudwatch_math_expression',
    #             # 'create_cloudwatch_widget',
    #             'create_sns_topic',
    #             'is_construct',
    #             'node',
    #             'to_string'
    #         ])
    #     )
