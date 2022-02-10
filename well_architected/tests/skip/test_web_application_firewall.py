from tests.utilities import TestTemplates, true, false

class TestWebApplicationFirewall(TestTemplates):

    def test_web_application_firewall(self):
        self.assert_template_equal(
            'WebApplicationFirewall'
        )