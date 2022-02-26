from tests.utilities import TestTemplates, true, false

class TestWellArchitectedPatterns(TestTemplates):

    @staticmethod
    def patterns():
        return (
            'BigFan',
            'DestinedLambda',
            'DynamoDBFlow',
            'DynamoDBTable',
            'EventBridgeCircuitBreaker',
            'EventBridgeEtl',
            'FatLambda',
            'HitCounter',
            'HttpFlow',
            'LambdaCircuitBreaker',
            'LambdaHttpApiGateway',
            'LambdaLith',
            'LambdaRestAPIGateway',
            'RdsProxy',
            'ScalableWebhook',
            'SinglePurposeLambda',
            'SnsFlow',
            'SnsRestApi',
            'SNSTopic',
            'SqsFlow',
            'WebApplicationFirewall',
            'XRayTracerSnsFanOutTopic',
        )

    def test_well_architected_cdk_patterns(self):
        for pattern in self.patterns():
            with self.subTest(i=pattern):
                self.assert_template_equal(pattern)
