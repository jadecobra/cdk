import tests.utilities

class TestWellArchitectedPatterns(tests.utilities.TestTemplates):

    @staticmethod
    def patterns():
        return (
            'ApiSnsLambdaEventBridgeLambda',
            'ApiSnsSqsLambda',
            'ApiStepFunctions',
            'CircuitBreakerLambda',
            'RestApiDynamodb',
            'WafApiLambdaDynamodb',
            'SagaStepFunction',
            'SimpleGraphqlService',
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
            # 'RdsProxy',
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
