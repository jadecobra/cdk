import tests.utilities

class TestWellArchitectedPatterns(tests.utilities.TestTemplates):

    @staticmethod
    def patterns():
        return (
            # 'ApiLambdaRds',
            # 'ApiLambdaDynamodb',
            # 'ApiLambdaDynamodbEventBridgeLambda',
            'AutoscalingEcsService',
            'AutoscalingEcsServiceWithPlacement',
            'AutoscalingEcsCluster',
            'AlbAutoscalingEcsService',
            'NlbAutoscalingEcsService',
            'NlbFargateService',
            # 'ApiLambdaEventBridgeLambda',
            # 'ApiLambdaSqsLambdaDynamodb',
            # 'ApiSnsLambdaEventBridgeLambda',
            # 'ApiSnsSqsLambda',
            # 'ApiStepFunctions',
            # 'LambdaFat',
            # 'LambdaLith',
            # 'LambdaPowerTuner',
            # 'LambdaSinglePurpose',
            # 'RestApiDynamodb',
            # # 'RestApiSns',
            # 'S3SqsLambdaEcsEventBridgeLambdaDynamodb',
            # 'SagaStepFunction',
            # 'SimpleGraphqlService',
            # 'SnsLambda',
            # 'SnsLambdaSns',
            # 'SnsLambdaDynamodb',
            # 'SqsLambdaSqs',
            # 'WafApiLambdaDynamodb',
            # 'XRayTracerSnsFanOutTopic',
            # 'DynamoDBTable',
            # 'DynamoStreamer',
            # 'ApiLambdaFunction',
        )

    def test_well_architected_cdk_patterns(self):
        for pattern in self.patterns():
            with self.subTest(i=pattern):
                self.assert_template_equal(pattern)
