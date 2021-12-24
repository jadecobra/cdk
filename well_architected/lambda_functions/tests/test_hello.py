import hello

from unittest import TestCase

class TestHelloLambda(TestCase):

    def test_hello(self):
        self.assertEqual(
            hello.handler({}),
            {'statusCode': 200, 'body': 'Hello World'}
        )