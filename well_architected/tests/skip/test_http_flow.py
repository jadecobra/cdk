from tests.utilities import TestTemplates, true, false


class TestHttpFlow(TestTemplates):

    def test_http_flow(self):
        self.assert_template_equal(
            'HttpFlow'
        )