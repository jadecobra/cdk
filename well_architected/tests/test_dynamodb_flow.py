from tests.utilities import TestTemplates, true, false

class TestDynamoDBFlow(TestTemplates):

    def test_dynamodb_flow(self):
        self.assert_template_equal('DynamoDBFlow')