import unittest
import lambda_functions.fat_lambda.fat_lambda as fat_lambda
import random


class TestFatLambdaFunction(unittest.TestCase):

    first_number = random.randint(0, 1000000)
    second_number = random.randint(0, 1000000)

    def query_string_parameters(self):
        return {
            'queryStringParameters': {
                'firstNumber': self.first_number,
                'secondNumber': self.second_number,
            }
        }

    def test_extract_parameters(self):
        self.assertEqual(
            self.query_string_parameters()
            (self.first_number, self.second_number)
        )

    def test_multiply(self):
        self.assertEqual(
            fat_lambda.multiply(
                {
                    'queryStringParameters': {
                        'firstNumber': 1,
                        'secondNumber': 2,
                    }
                },
                None
            ),
            {
                'body': 2,
                'statusCode': 200,
            }
        )