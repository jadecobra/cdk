from tests.utilities import TestTemplates, true, false

class TestWellArchitectedPatterns(TestTemplates):

    def patterns(self):
        return (
            'DynamoDBFlow',
            'DynamoDBTable',
            'EventBridgeCircuitBreaker',
            'LambdaHttpApiGateway',
            'HttpFlow',
            'LambdaFunction',
            'LambdaRestAPIGateway',
            'SnsFlow',
            'SnsRestApi',
            'SNSTopic',
            'SqsFlow',
            'WebApplicationFirewall',
        )

    def test_well_architected_cdk_patterns(self):
        self.assertFalse(True)
        # for pattern in self.patterns():
        #     with self.subTest(i=pattern):
        #         self.assert_template_equal(pattern)


    # def test_well_architected_patterns(self):
    #     self.assert_template_equal('DynamoDBFlow')
    #     self.assert_template_equal('DynamoDBTable')
    #     self.assert_template_equal('EventBridgeCircuitBreaker')
    #     self.assert_template_equal('LambdaHttpApiGateway')
    #     self.assert_template_equal('HttpFlow')
    #     self.assert_template_equal('LambdaFunction')
    #     self.assert_template_equal('LambdaRestAPIGateway')
    #     self.assert_template_equal('SnsFlow')
    #     self.assert_template_equal('SnsRestApi')
    #     self.assert_template_equal('SNSTopic')
    #     self.assert_template_equal('SqsFlow')
    #     self.assert_template_equal('WebApplicationFirewall')
