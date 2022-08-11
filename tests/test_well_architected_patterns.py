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
        result = tests.utilities.time_it(
            subprocess.run,
            (
                'cdk ls --app python3 src/well_architected/app.py '
                '--version-reporting=false'
                '--path-metadata=false --asset-metadata=false'
            ),
            description=f'cdk ls',
            shell=True,
            capture_output=True,
        )
        print(result.stderr.decode())
        print(result.stdout.decode())
        self.assertNotEqual(result.returncode, 1)
        for pattern in self.patterns():
            with self.subTest(i=pattern):
                self.assert_template_equal(pattern)

    def test_cdk_returncode(self):
        result = subprocess.run(
            'cdk ls --app python3 src/app.py',
            shell=True,
            capture_output=True
        )
        # self.assertEqual(
        #     result.stderr, b'\n'
        #     # (
        #     #     b'\n--app is required either in command-line, '
        #     #     b'in cdk.json or in ~/.cdk.json\n'
        #     # )
        # )
        self.assertEqual(result.stdout, b'')
        self.assertEqual(result.returncode, 1)
        # with self.assertRaises(subprocess.CalledProcessError):
        #     result.check_returncode()