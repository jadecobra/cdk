from tests.utilities import TestTemplates, true, false


class TestXRayTracer(TestTemplates):

    def test_sns_rest_api(self):
        self.assert_template_equal(
            'SnsRestApi'
        )