import unittest
import lambda_functions.lambda_fat.lambda_fat as lambda_fat
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

    def test_get_first_number(self):
        self.assertEqual(
            lambda_fat.get_first_number(self.query_string_parameters()),
            self.first_number
        )

    def test_get_second_number(self):
        self.assertEqual(
            lambda_fat.get_second_number(self.query_string_parameters()),
            self.second_number
        )

    def test_multiply(self):
        self.assertEqual(
            lambda_fat.multiply(
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
            lambda_fat.add(
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
            lambda_fat.subtract(
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