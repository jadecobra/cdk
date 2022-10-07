import subprocess
import jadecobra.toolkit


class TestWellArchitectedPatterns(jadecobra.toolkit.TestCase):

    @staticmethod
    def patterns():
        return (
            'ApiLambdaDynamodb',
            'ApiLambdaDynamodbEventBridgeLambda',
            'ApiLambdaEventBridgeLambda',
            'ApiLambdaRds',
            'ApiLambdaSqsLambdaDynamodb',
            'ApiStepFunctions',
            'LambdaFat',
            'LambdaLith',
            'LambdaPowerTuner',
            'LambdaSinglePurpose',
            'RestApiDynamodb', # Can we do these with an HTTP API
            'RestApiSns',
            'RestApiSnsLambdaEventBridgeLambda',
            'RestApiSnsSqsLambda',
            'RestApiSns',
            'S3SqsLambdaEcsEventBridgeLambdaDynamodb',
            'SagaStepFunction',
            'SimpleGraphqlService',
            'SnsLambda',
            'SnsLambdaSns',
            'SnsLambdaDynamodb',
            'SqsLambdaSqs',
            'WafApiLambdaDynamodb',
        )

    def test_well_architected_cdk_patterns(self):
        self.create_cdk_templates()
        for pattern in self.patterns():
            with self.subTest(i=pattern):
                self.assert_cdk_templates_equal(pattern)