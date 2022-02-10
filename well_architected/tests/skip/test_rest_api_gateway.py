from tests.utilities import TestTemplates, true, false


class TestRestAPIGateway(TestTemplates):

    def test_rest_api_gateway(self):
        self.assert_template_equal(
            'LambdaRestAPIGateway'
        )