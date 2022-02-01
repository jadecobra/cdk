from tests.utilities import TestTemplates, true, false


class TestSNSTopic(TestTemplates):

    def test_sns_topic(self):
        self.assert_template_equal(
            'SNSTopic',
            {
              "Resources": {
                "SnsTopic2C1570A4": {
                  "Type": "AWS::SNS::Topic"
                }
              },
              "Outputs": {
                "ExportsOutputRefSnsTopic2C1570A4EE4BCC49": {
                  "Value": {
                    "Ref": "SnsTopic2C1570A4"
                  },
                  "Export": {
                    "Name": "SnsTopic:ExportsOutputRefSnsTopic2C1570A4EE4BCC49"
                  }
                }
              }
            }
        )