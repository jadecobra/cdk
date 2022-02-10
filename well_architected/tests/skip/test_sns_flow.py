from tests.utilities import TestTemplates, true, false


class TestSnsFlow(TestTemplates):

    def test_sns_flow(self):
        self.assert_template_equal(
            'SnsFlow'
        )