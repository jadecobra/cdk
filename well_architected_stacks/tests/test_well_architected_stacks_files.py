import jadecobra.toolkit
import src.well_architected_stacks
import os


class TestWellArchitectedConstructs(jadecobra.toolkit.TestCase):

    def test_well_architected_stacks_files(self):
        self.assertEqual(
            sorted(os.listdir('src/well_architected_stacks')),
            [
                '__init__.py',
                '__pycache__',
                'api_lambda_dynamodb.py',
                'api_lambda_dynamodb_eventbridge_lambda.py',
                'api_lambda_eventbridge_lambda.py',
                'api_lambda_rds.py',
                'api_lambda_sqs_lambda_dynamodb.py',
                'api_step_functions.py',
                'lambda_power_tuner.py',
                'lambda_trilogy',
                'rest_api_dynamodb.py',
                'rest_api_sns.py',
                'rest_api_sns_lambda_eventbridge_lambda.py',
                'rest_api_sns_sqs_lambda.py',
                's3_sqs_lambda_ecs_eventbridge_lambda_dynamodb.py',
                'saga_step_function.py',
                'simple_graphql_service',
                'sns_lambda.py',
                'sns_lambda_dynamodb.py',
                'sns_lambda_sns.py',
                'sns_topic.py',
                'sqs_lambda_sqs.py',
                'waf_rest_api_lambda_dynamodb.py',
                'well_architected_app.py',
                'well_architected_stack.py'
            ]
        )

    def test_well_architected_stacks_attributes(self):
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
                '__spec__',
                'api_lambda_dynamodb',
                'api_lambda_dynamodb_eventbridge_lambda',
                'api_lambda_eventbridge_lambda',
                'api_lambda_rds',
                'api_lambda_sqs_lambda_dynamodb',
                'api_step_functions',
                'lambda_power_tuner',
                'lambda_trilogy',
                'rest_api_dynamodb',
                'rest_api_sns',
                'rest_api_sns_lambda_eventbridge_lambda',
                'rest_api_sns_sqs_lambda',
                's3_sqs_lambda_ecs_eventbridge_lambda_dynamodb',
                'saga_step_function',
                'simple_graphql_service',
                'sns_lambda',
                'sns_lambda_dynamodb',
                'sns_lambda_sns',
                'sns_topic',
                'sqs_lambda_sqs',
                'waf_rest_api_lambda_dynamodb',
                'well_architected_stack'
            ]
        )