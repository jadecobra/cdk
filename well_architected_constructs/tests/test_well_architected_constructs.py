import jadecobra.toolkit
import src.well_architected_constructs as well_architected_constructs
import os


class TestWellArchitectedConstructsFiles(jadecobra.toolkit.TestCase):

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