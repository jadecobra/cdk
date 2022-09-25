import subprocess
import jadecobra.toolkit


class TestWellArchitectedPatterns(jadecobra.toolkit.TestCase):

    @staticmethod
    def patterns():
        return (
            'AutoscalingEcsService',
            'AutoscalingEcsServiceWithPlacement',
            'AutoscalingEcsCluster',
            'AlbAutoscalingEcsService',
            'NlbAutoscalingEcsService',
            'AlbFargateService',
            'NlbFargateService',
            'NlbAutoscalingFargateService',
        )

    def test_well_architected_cdk_patterns(self):
        result = jadecobra.toolkit.time_it(
            subprocess.run,
            (
                'cdk ls *Ecs*'
                '--no-version-reporting '
                '--no-path-metadata '
                '--no-asset-metadata'
            ),
            description=f'cdk ls',
            shell=True,
            capture_output=True,
        )
        print(result.stderr.decode())
        print(result.stdout.decode())
        self.assertEqual(result.returncode, 0)
        for pattern in self.patterns():
            with self.subTest(i=pattern):
                self.assert_cdk_templates_equal(pattern)