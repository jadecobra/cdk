import jadecobra.toolkit
import src.well_architected.well_architected_constructs
import os


class TestWellArchitectedConstructs(jadecobra.toolkit.TestCase):

    def test_well_architected_constructs_attributes(self):
        self.assertEqual(
            sorted(os.listdir('src/well_architected/well_architected_constructs')),
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
        # self.assert_attributes_equal(
        #     src.well_architected.well_architected_constructs,
        #     []
        # )