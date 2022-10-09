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
            'SeleniumTestService',
            'BatchEC2Stack',
            'AlexaSkill'
        )

    def test_well_architected_cdk_patterns(self):
        self.create_cdk_templates()
        for pattern in self.patterns():
            with self.subTest(i=pattern):
                self.assert_cdk_templates_equal(pattern)