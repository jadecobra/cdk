from tests.utilities import TestTemplates, true, false

class TestDynamoDBTable(TestTemplates):

    def test_dynamodb_table(self):
        self.assert_template_equal(
            'DynamoDBTable',
            {
  "Resources": {
    "Hits9BF577DE": {
      "Type": "AWS::DynamoDB::Table",
      "Properties": {
        "KeySchema": [
          {
            "AttributeName": "path",
            "KeyType": "HASH"
          }
        ],
        "AttributeDefinitions": [
          {
            "AttributeName": "path",
            "AttributeType": "S"
          }
        ],
        "BillingMode": "PAY_PER_REQUEST"
      },
      "UpdateReplacePolicy": "Retain",
      "DeletionPolicy": "Retain",
      "Metadata": {
        "aws:cdk:path": "DynamoDBTable/Hits/Hits/Resource"
      }
    },
    "HitsDynamoDBUserErrors07CE7B5C5": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Fn::ImportValue": "SnsTopic:ExportsOutputRefSnsTopic2C1570A4EE4BCC49"
          }
        ],
        "DatapointsToAlarm": 1,
        "MetricName": "UserErrors",
        "Namespace": "AWS/DynamoDB",
        "Period": 300,
        "Statistic": "Sum",
        "Threshold": 0,
        "TreatMissingData": "notBreaching"
      },
      "Metadata": {
        "aws:cdk:path": "DynamoDBTable/Hits/DynamoDB User Errors > 0/Resource"
      }
    },
    "HitsDynamoDBTableReadsWritesThrottledA2E6A6CD": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Fn::ImportValue": "SnsTopic:ExportsOutputRefSnsTopic2C1570A4EE4BCC49"
          }
        ],
        "DatapointsToAlarm": 1,
        "Metrics": [
          {
            "Expression": "m1 + m2",
            "Id": "expr_1",
            "Label": "DynamoDB Throttles"
          },
          {
            "Id": "m1",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "TableName",
                    "Value": {
                      "Ref": "Hits9BF577DE"
                    }
                  }
                ],
                "MetricName": "ReadThrottleEvents",
                "Namespace": "AWS/DynamoDB"
              },
              "Period": 300,
              "Stat": "Sum"
            },
            "ReturnData": false
          },
          {
            "Id": "m2",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "TableName",
                    "Value": {
                      "Ref": "Hits9BF577DE"
                    }
                  }
                ],
                "MetricName": "WriteThrottleEvents",
                "Namespace": "AWS/DynamoDB"
              },
              "Period": 300,
              "Stat": "Sum"
            },
            "ReturnData": false
          }
        ],
        "Threshold": 1,
        "TreatMissingData": "notBreaching"
      },
      "Metadata": {
        "aws:cdk:path": "DynamoDBTable/Hits/DynamoDB Table Reads--Writes Throttled/Resource"
      }
    },
    "HitsCloudWatchDashBoardD0EE794E": {
      "Type": "AWS::CloudWatch::Dashboard",
      "Properties": {
        "DashboardBody": {
          "Fn::Join": [
            "",
            [
              "{\"widgets\":[{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":0,\"properties\":{\"view\":\"timeSeries\",\"title\":\"DynamoDB Latency\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":true,\"metrics\":[[\"AWS/DynamoDB\",\"SuccessfulRequestLatency\",\"Operation\",\"GetItem\",\"TableName\",\"",
              {
                "Ref": "Hits9BF577DE"
              },
              "\"],[\"AWS/DynamoDB\",\"SuccessfulRequestLatency\",\"Operation\",\"UpdateItem\",\"TableName\",\"",
              {
                "Ref": "Hits9BF577DE"
              },
              "\"],[\"AWS/DynamoDB\",\"SuccessfulRequestLatency\",\"Operation\",\"PutItem\",\"TableName\",\"",
              {
                "Ref": "Hits9BF577DE"
              },
              "\"],[\"AWS/DynamoDB\",\"SuccessfulRequestLatency\",\"Operation\",\"DeleteItem\",\"TableName\",\"",
              {
                "Ref": "Hits9BF577DE"
              },
              "\"],[\"AWS/DynamoDB\",\"SuccessfulRequestLatency\",\"Operation\",\"Query\",\"TableName\",\"",
              {
                "Ref": "Hits9BF577DE"
              },
              "\"]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":6,\"properties\":{\"view\":\"timeSeries\",\"title\":\"DynamoDB Consumed Read/Write Units\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":false,\"metrics\":[[\"AWS/DynamoDB\",\"ConsumedReadCapacityUnits\",\"TableName\",\"",
              {
                "Ref": "Hits9BF577DE"
              },
              "\"],[\"AWS/DynamoDB\",\"ConsumedWriteCapacityUnits\",\"TableName\",\"",
              {
                "Ref": "Hits9BF577DE"
              },
              "\"]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":12,\"properties\":{\"view\":\"timeSeries\",\"title\":\"DynamoDB Throttles\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":true,\"metrics\":[[\"AWS/DynamoDB\",\"ReadThrottleEvents\",\"TableName\",\"",
              {
                "Ref": "Hits9BF577DE"
              },
              "\",{\"stat\":\"Sum\"}],[\"AWS/DynamoDB\",\"WriteThrottleEvents\",\"TableName\",\"",
              {
                "Ref": "Hits9BF577DE"
              },
              "\",{\"stat\":\"Sum\"}]],\"yAxis\":{}}}]}"
            ]
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "DynamoDBTable/Hits/CloudWatchDashBoard/Resource"
      }
    },
    "CDKMetadata": {
      "Type": "AWS::CDK::Metadata",
      "Properties": {
        "Analytics": "v2:deflate64:H4sIAAAAAAAA/02MTQqDMBCFz+I+jgZX3bXYAxTtBcYkxVTNQDJBJOTurQqlq/e9H54E2VygLq64hlLpqUqKvIHUM6pJtOQC+6hYdCZQ9MqI9uX++bvQli25LPaHpDeHC+kB0hOH+ZgckIWaKeoVWY2QbjP6Ze9OuGMYB0Kv9+hncs7isfFIrmpA1iCLd7C29NGxXQx0p34AQPlDxsEAAAA="
      },
      "Metadata": {
        "aws:cdk:path": "DynamoDBTable/CDKMetadata/Default"
      },
      "Condition": "CDKMetadataAvailable"
    }
  },
  "Conditions": {
    "CDKMetadataAvailable": {
      "Fn::Or": [
        {
          "Fn::Or": [
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "af-south-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "ap-east-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "ap-northeast-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "ap-northeast-2"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "ap-south-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "ap-southeast-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "ap-southeast-2"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "ca-central-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "cn-north-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "cn-northwest-1"
              ]
            }
          ]
        },
        {
          "Fn::Or": [
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "eu-central-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "eu-north-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "eu-south-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "eu-west-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "eu-west-2"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "eu-west-3"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "me-south-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "sa-east-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "us-east-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "us-east-2"
              ]
            }
          ]
        },
        {
          "Fn::Or": [
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "us-west-1"
              ]
            },
            {
              "Fn::Equals": [
                {
                  "Ref": "AWS::Region"
                },
                "us-west-2"
              ]
            }
          ]
        }
      ]
    }
  },
  "Outputs": {
    "ExportsOutputFnGetAttHits9BF577DEArnFF8B7C1B": {
      "Value": {
        "Fn::GetAtt": [
          "Hits9BF577DE",
          "Arn"
        ]
      },
      "Export": {
        "Name": "DynamoDBTable:ExportsOutputFnGetAttHits9BF577DEArnFF8B7C1B"
      }
    },
    "ExportsOutputRefHits9BF577DEBF202F48": {
      "Value": {
        "Ref": "Hits9BF577DE"
      },
      "Export": {
        "Name": "DynamoDBTable:ExportsOutputRefHits9BF577DEBF202F48"
      }
    }
  }
}
        )