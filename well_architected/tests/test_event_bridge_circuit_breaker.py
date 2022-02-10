from tests.utilities import TestTemplates, true, false

class TestEventBridgeCircuitBreaker(TestTemplates):

    def test_event_bridge_circuit_breaker(self):
        self.assert_template_equal(
            'EventBridgeCircuitBreaker',
        )