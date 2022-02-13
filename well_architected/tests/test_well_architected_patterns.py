from tests.utilities import TestTemplates, true, false

class TestWellArchitectedPatterns(TestTemplates):

    def test_dynamodb_flow(self):
        self.assert_template_equal('DynamoDBFlow')

    def test_dynamodb_table(self):
        self.assert_template_equal(
            'DynamoDBTable',
        )

    def test_event_bridge_circuit_breaker(self):
        self.assert_template_equal(
            'EventBridgeCircuitBreaker',
        )

    def test_http_api_gateway(self):
        self.assert_template_equal(
            'LambdaHttpApiGateway'
        )

    def test_http_flow(self):
        self.assert_template_equal(
            'HttpFlow'
        )

    def test_lambda_function(self):
        self.assert_template_equal(
            'LambdaFunction'
        )

    def test_rest_api_gateway(self):
        self.assert_template_equal(
            'LambdaRestAPIGateway'
        )

    def test_sns_flow(self):
        self.assert_template_equal(
            'SnsFlow'
        )

    def test_sns_rest_api(self):
        self.assert_template_equal(
            'SnsRestApi'
        )

    def test_sns_topic(self):
        self.assert_template_equal(
            'SNSTopic'
        )

    def test_sqs_flow(self):
        self.assert_template_equal(
            'SqsFlow'
        )

    def test_web_application_firewall(self):
        self.assert_template_equal(
            'WebApplicationFirewall'
        )

    