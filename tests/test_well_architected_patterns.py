import tests.utilities

class TestWellArchitectedPatterns(tests.utilities.TestTemplates):

    @staticmethod
    def patterns():
        return (
            'ApiSnsLambdaEventBridgeLambda',
            'ApiSnsSqsLambda',
            'ApiStepFunctions',
            'CircuitBreakerEventBridge',
            'CircuitBreakerLambda',
            'EventBridgeAtm',
            'EventBridgeEtl',
            'LambdaFat',
            'LambdaLith',
            'LambdaSinglePurpose',
            'RestApiDynamodb',
            'SagaStepFunction',
            'SimpleGraphqlService',
            'SnsRestApi',
            'SnsLambdaDynamodb',
            'SnsFlow',
            'SqsFlow',
            'WafApiLambdaDynamodb',
            'XRayTracerSnsFanOutTopic',
            # 'DynamoDBTable',
            # 'DynamoStreamer',
            # 'HitCounter',
            # 'HttpFlow',
            # 'LambdaPowerTuner',
            # 'RdsProxy',
            # 'SNSTopic',
            # 'HttpApiLambdaFunction',
            # 'HttpApiStateMachine',
        )

    def test_well_architected_cdk_patterns(self):
        for pattern in self.patterns():
            with self.subTest(i=pattern):
                self.assert_template_equal(pattern)
