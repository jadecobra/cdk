import tests.utilities

class TestWellArchitectedPatterns(tests.utilities.TestTemplates):

    @staticmethod
    def patterns():
        return (
            'ApiLambdaRds',
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
            'RestApiSns',
            'SagaStepFunction',
            'SimpleGraphqlService',
            'SnsLambda',
            'SnsLambdaSns',
            'SnsLambdaDynamodb',
            'SqsLambdaSqs',
            'WafApiLambdaDynamodb',
            'XRayTracerSnsFanOutTopic',
            # 'DynamoDBTable',
            # 'DynamoStreamer',
            # 'HitCounter',
            # 'LambdaPowerTuner',
            # 'SNSTopic',
            # 'HttpApiLambdaFunction',
            # 'HttpApiStateMachine',
        )

    def test_well_architected_cdk_patterns(self):
        for pattern in self.patterns():
            with self.subTest(i=pattern):
                self.assert_template_equal(pattern)
