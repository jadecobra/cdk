from tests.utilities import TestTemplates, true, false

class TestDynamoDBTable(TestTemplates):

    def test_dynamodb_table(self):
        self.assert_template_equal(
            'DynamoDBTable',
        )