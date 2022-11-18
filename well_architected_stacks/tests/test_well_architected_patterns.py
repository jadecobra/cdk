import subprocess
import jadecobra.toolkit


class TestWellArchitectedPatterns(jadecobra.toolkit.TestCase):

    @staticmethod
    def patterns():
        return (
            'HttpApiLambdaDynamodb',
            'RestApiLambdaDynamodb',
            'HttpApiLambdaDynamodbEventBridgeLambda',
            'RestApiLambdaDynamodbEventBridgeLambda',
            'HttpApiLambdaEventBridgeLambda',
            'RestApiLambdaEventBridgeLambda',
            'HttpApiLambdaRds',
            'RestApiLambdaRds',
            'HttpApiLambdaSqsLambdaDynamodb',
            'RestApiLambdaSqsLambdaDynamodb',
            'HttpApiStepFunctions',
            'RestApiStepFunctions',
            'HttpApiLambdaLith',
            'RestApiLambdaLith',
            'HttpApiLambdaFat',
            'RestApiLambdaFat',
            'LambdaPowerTuner',
            'HttpApiLambdaSinglePurpose',
            'RestApiLambdaSinglePurpose',
            'RestApiDynamodb',
            'RestApiSns',
            'RestApiSnsLambdaEventBridgeLambda',
            'RestApiSnsSqsLambda',
            'RestApiSns',
            # 'S3SqsLambdaEcsEventBridgeLambdaDynamodb',
            # 'SimpleGraphqlService',
            # 'SnsLambda',
            'SnsLambdaSns',
            # 'SnsLambdaDynamodb',
            'SqsLambdaSqs',
            # 'HttpApiSagaStepFunction',
            # 'RestApiSagaStepFunction',
            'WafRestApiLambdaDynamodb',
        )

    def test_well_architected_cdk_patterns(self):
        self.create_cdk_templates()
        for pattern in self.patterns():
            with self.subTest(i=pattern):
                self.assert_cdk_templates_equal(pattern)