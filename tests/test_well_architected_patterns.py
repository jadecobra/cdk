import tests.utilities
import os
import subprocess

class TestWellArchitectedPatterns(tests.utilities.TestTemplates):

    @staticmethod
    def patterns():
        return (
            'ApiLambdaRds',
            'ApiLambdaDynamodb',
            'ApiLambdaDynamodbEventBridgeLambda',
            'AutoscalingEcsService',
            'AutoscalingEcsServiceWithPlacement',
            'AutoscalingEcsCluster',
            'AlbAutoscalingEcsService',
            'NlbAutoscalingEcsService',
            'NlbFargateService',
            'NlbAutoscalingFargateService',
            'ApiLambdaEventBridgeLambda',
            'ApiLambdaSqsLambdaDynamodb',
            'ApiSnsLambdaEventBridgeLambda',
            'ApiSnsSqsLambda',
            'ApiStepFunctions',
            'LambdaFat',
            'LambdaLith',
            'LambdaPowerTuner',
            'LambdaSinglePurpose',
            'RestApiDynamodb',
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
        tests.utilities.time_it(
            os.system,
            (
                '.src/cdk ls --version-reporting=false'
                '--path-metadata=false --asset-metadata=false'
            ),
            description=f'cdk.ls()'
        )
        for pattern in self.patterns():
            with self.subTest(i=pattern):
                self.assert_template_equal(pattern)

    def test_cdk_returncode(self):
        result = subprocess.run('./src/cdk ls', shell=True)
        self.assertEqual(
            dir(result),
            [
                '__class__',
                '__class_getitem__',
                '__delattr__',
                '__dict__',
                '__dir__',
                '__doc__',
                '__eq__',
                '__format__',
                '__ge__',
                '__getattribute__',
                '__gt__',
                '__hash__',
                '__init__',
                '__init_subclass__',
                '__le__',
                '__lt__',
                '__module__',
                '__ne__',
                '__new__',
                '__reduce__',
                '__reduce_ex__',
                '__repr__',
                '__setattr__',
                '__sizeof__',
                '__str__',
                '__subclasshook__',
                '__weakref__',
                'args',
                'check_returncode',
                'returncode',
                'stderr',
                'stdout'
            ]
        )
        self.assertIsNone(result.stderr)
        self.assertIsNone(result.stdout)
        self.assertIsNone(result.check_returncode())