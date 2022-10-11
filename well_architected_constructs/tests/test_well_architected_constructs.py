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


class TestWellArchitectedConstructAttributes(jadecobra.toolkit.TestCase):

    @staticmethod
    def cloudwatch_attributes():
        return (
            'cloudwatch_math_sum',
            'create_cloudwatch_alarm',
            'create_cloudwatch_math_expression',
            'create_cloudwatch_widget',
            'create_cloudwatch_widgets',
        )

    def well_architected_construct_attributes(self):
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
            'create_sns_topic',
            'is_construct',
            'node',
            'to_string',
            *self.cloudwatch_attributes(),
        )

# TODO
# Abstract ApiLambdaDynnamoDb to use ApiLambda inheritance
# Can StepFunctions use RestApi?
# Can Sns use HttpApi?