import tests.utilities

class TestWellArchitectedPatterns(tests.utilities.TestTemplates):

    @staticmethod
    def patterns():
        return (
            'ApiLambdaRds',
            'ApiLambdaDynamodb',
            'ApiLambdaEventBridgeLambda',
            'ApiSnsLambdaEventBridgeLambda',
            'ApiSnsSqsLambda',
            'ApiStepFunctions',
            'CircuitBreakerEventBridge',
            'EventBridgeEtl',
            'LambdaFat',
            'LambdaLith',
            'LambdaPowerTuner',
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
            # 'SNSTopic',
            # 'HttpApiLambdaFunction',
            # 'HttpApiStateMachine',
        )

    def test_well_architected_cdk_patterns(self):
        for pattern in self.patterns():
            with self.subTest(i=pattern):
                self.assert_template_equal(pattern)
