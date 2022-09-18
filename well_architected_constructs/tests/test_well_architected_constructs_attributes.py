import jadecobra.toolkit
import src.well_architected_constructs as well_architected_constructs

from  tests.test_well_architected_constructs import TestWellArchitectedConstructAttributes


class TestConstructAttributes(TestWellArchitectedConstructAttributes):

    def test_dynamodb_table(self):
        self.assert_attributes_equal(
            well_architected_constructs.dynamodb_table.DynamodbTableConstruct,
            [
                *self.well_architected_construct_attributes(),
                'create_latency_widget',
                'create_read_write_capacity_widget',
                'create_system_errors_alarm',
                'create_throttles_alarm',
                'create_throttles_metric',
                'create_throttles_widget',
                'create_user_errors_alarm',
                'get_dynamodb_key',
                'get_dynamodb_metric',
            ]
        )

    def test_lambda_function(self):
        self.assert_attributes_equal(
            well_architected_constructs.lambda_function.LambdaFunctionConstruct,
            [
                *self.well_architected_construct_attributes(),
                'add_event_bridge_rule',
                'add_sns_trigger',
                'create_aws_sdk_layer',
                'create_invocation_longer_than_1_second_alarm',
                'create_invocations_error_greater_than_2_percent_alarm',
                'create_lambda_duration_widget',
                'create_lambda_error_percentage_metric',
                'create_lambda_error_percentage_widget',
                'create_lambda_throttled_percentage_metric',
                'create_lambda_throttled_percentage_widget',
                'create_layer',
                'create_layers',
                'create_throttled_invocations_greater_than_2_percent_alarm',
                'get_lambda_function_metric',
                'to_camel_case',
            ]
        )

    def test_sns_lambda(self):
        self.assert_attributes_equal(
            well_architected_constructs.sns_lambda.SnsLambdaConstruct,
            list(self.well_architected_construct_attributes()),
        )

    def test_web_application_firewall(self):
        self.assert_attributes_equal(
            well_architected_constructs.web_application_firewall.WebApplicationFirewall,
            [
                *self.well_architected_construct_attributes(),
                'add_geoblock_rule',
                'anonymous_ip_rule',
                'common_ruleset',
                'country_codes',
                'create_managed_rule',
                'create_managed_rule_group_statement',
                'create_visibility_configuration',
                'create_web_application_firewall',
                'create_web_application_firewall_association',
                'restricted_ip_list_rule',
                'web_application_firewall_rules'
            ]
        )
