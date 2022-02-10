from tests.utilities import TestTemplates, true, false


class TestSNSTopic(TestTemplates):

    def test_sns_topic(self):
        self.assert_template_equal(
            'SNSTopic'
        )