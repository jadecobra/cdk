import jadecobra.toolkit
import src.well_architected_stacks
import os


class TestWellArchitectedConstructs(jadecobra.toolkit.TestCase):

    def test_well_architected_constructs_files(self):
        self.assertEqual(
            sorted(os.listdir('src/well_architected_stacks')),
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
                'web_application_firewall.py'
            ]
        )

    def test_well_architected_constructs_attributes(self):
        self.assert_attributes_equal(
            src.well_architected_stacks,
            [
                '__builtins__',
                '__cached__',
                '__doc__',
                '__file__',
                '__loader__',
                '__name__',
                '__package__',
                '__path__',
                '__spec__'
            ]
        )