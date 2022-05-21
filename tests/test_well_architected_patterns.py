import tests.utilities

class TestWellArchitectedPatterns(tests.utilities.TestTemplates):

    @staticmethod
    def patterns():
        return (
            # 'ApiSnsLambdaEventBridgeLambda',
            # "ApiDynamodb",
            # "ApiStepFunctions",
            'CircuitBreakerLambda',
            # 'WafApiLambdaDynamodb',
            # 'SimpleGraphqlService',
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
            # 'LambdaPowerTuner',
            # 'LambdaLith',
            # 'LambdaRestAPIGateway',
            # 'RdsProxy',
            # 'SagaStepFunction',
            # 'SinglePurposeLambda',
            # 'SnsFlow',
            # 'SnsRestApi',
            # 'SNSTopic',
            # 'SqsFlow',
            # 'HttpApiLambdaFunction',
            # 'HttpApiStateMachine',
            # 'XRayTracerSnsFanOutTopic',
        )

    def test_well_architected_cdk_patterns(self):
        for pattern in self.patterns():
            with self.subTest(i=pattern):
                self.assert_template_equal(pattern)
