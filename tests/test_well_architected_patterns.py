import tests.utilities

class TestWellArchitectedPatterns(tests.utilities.TestTemplates):

    @staticmethod
    def patterns():
        return (
            'ApiSnsLambdaEventBridgeLambda',
            # "ApiDynamodb",
            # "ApiStepFunctions",
            # 'BigFan',
            # 'DynamoDBFlow',
            # 'DynamoDBTable',
            # 'DynamoStreamer',
            # 'EventBridgeAtm',
            # 'EventBridgeCircuitBreaker',
            # 'EventBridgeEtl',
            # 'FatLambda',
            # 'HitCounter',
            # 'HttpFlow',
            # 'LambdaCircuitBreaker',
            # 'LambdaPowerTuner',
            # 'LambdaLith',
            # 'LambdaRestAPIGateway',
            # 'RdsProxy',
            # 'SagaStepFunction',
            # 'SinglePurposeLambda',
            # 'SimpleGraphqlService',
            # 'SnsFlow',
            # 'SnsRestApi',
            # 'SNSTopic',
            # 'SqsFlow',
            # 'HttpApiLambdaFunction',
            # 'HttpApiStateMachine',
            # 'XRayTracerSnsFanOutTopic',
            # 'WafApiLambdaDynamodb',
        )

    def test_well_architected_cdk_patterns(self):
        for pattern in self.patterns():
            with self.subTest(i=pattern):
                self.assert_template_equal(pattern)
