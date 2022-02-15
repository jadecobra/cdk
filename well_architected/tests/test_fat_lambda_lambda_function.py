import unittest
import lambda_functions.fat_lambda.fat_lambda as fat_lambda
import random


def random_number():
    return random.randint(-10000000, 10000000)

class TestFatLambdaFunction(unittest.TestCase):

    first_number = random_number()
    second_number = random_number()

    def query_string_parameters(self):
        return {
            'queryStringParameters': {
                'firstNumber': self.first_number,
                'secondNumber': self.second_number,
            }
        }

    def test_extract_parameters(self):
        self.assertEqual(
            fat_lambda.extract_parameters(self.query_string_parameters()),
            (self.first_number, self.second_number)
        )

    def test_multiply(self):
        self.assertEqual(
            fat_lambda.multiply(
                {
                    'queryStringParameters': {
                        'firstNumber': self.first_number,
                        'secondNumber': self.second_number,
                    }
                },
                None
            ),
            {
                'body': self.first_number * self.second_number,
                'statusCode': 200,
            }
        )

    def test_add(self):
        self.assertEqual(
            fat_lambda.add(
                {
                    'queryStringParameters': {
                        'firstNumber': self.first_number,
                        'secondNumber': self.second_number,
                    }
                },
                None
            ),
            {
                'body': self.first_number + self.second_number,
                'statusCode': 200,
            }
        )

    def test_subtract(self):
        self.assertEqual(
            fat_lambda.subtract(
                {
                    'queryStringParameters': {
                        'firstNumber': self.first_number,
                        'secondNumber': self.second_number,
                    }
                },
                None
            ),
            {
                'body': self.first_number - self.second_number,
                'statusCode': 200,
            }
        )