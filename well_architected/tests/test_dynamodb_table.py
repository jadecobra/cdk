from tests.utilities import TestTemplates, true, false

class TestDynamoDBTable(TestTemplates):

    def test_cloudwatch_dashboard(self):
        self.assert_template_equal(
            'DynamoDBTable',
            {
  "Resources": {
    "HitsFF5AF8CD": {
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
        "aws:cdk:path": "DynamoDBTable/Hits/Resource"
      }
    },
    "DynamoDBUserErrors063AAE77E": {
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
        "aws:cdk:path": "DynamoDBTable/DynamoDB User Errors > 0/Resource"
      }
    },
    "DynamoDBTableReadsWritesThrottled13F6F2AE": {
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
                      "Ref": "HitsFF5AF8CD"
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
                      "Ref": "HitsFF5AF8CD"
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
        "aws:cdk:path": "DynamoDBTable/DynamoDB Table Reads--Writes Throttled/Resource"
      }
    },
    "CloudWatchDashBoard043C60B6": {
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
                "Ref": "HitsFF5AF8CD"
              },
              "\"],[\"AWS/DynamoDB\",\"SuccessfulRequestLatency\",\"Operation\",\"UpdateItem\",\"TableName\",\"",
              {
                "Ref": "HitsFF5AF8CD"
              },
              "\"],[\"AWS/DynamoDB\",\"SuccessfulRequestLatency\",\"Operation\",\"PutItem\",\"TableName\",\"",
              {
                "Ref": "HitsFF5AF8CD"
              },
              "\"],[\"AWS/DynamoDB\",\"SuccessfulRequestLatency\",\"Operation\",\"DeleteItem\",\"TableName\",\"",
              {
                "Ref": "HitsFF5AF8CD"
              },
              "\"],[\"AWS/DynamoDB\",\"SuccessfulRequestLatency\",\"Operation\",\"Query\",\"TableName\",\"",
              {
                "Ref": "HitsFF5AF8CD"
              },
              "\"]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":6,\"properties\":{\"view\":\"timeSeries\",\"title\":\"DynamoDB Consumed Read/Write Units\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":false,\"metrics\":[[\"AWS/DynamoDB\",\"ConsumedReadCapacityUnits\",\"TableName\",\"",
              {
                "Ref": "HitsFF5AF8CD"
              },
              "\"],[\"AWS/DynamoDB\",\"ConsumedWriteCapacityUnits\",\"TableName\",\"",
              {
                "Ref": "HitsFF5AF8CD"
              },
              "\"]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":12,\"properties\":{\"view\":\"timeSeries\",\"title\":\"DynamoDB Throttles\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":true,\"metrics\":[[\"AWS/DynamoDB\",\"ReadThrottleEvents\",\"TableName\",\"",
              {
                "Ref": "HitsFF5AF8CD"
              },
              "\",{\"stat\":\"Sum\"}],[\"AWS/DynamoDB\",\"WriteThrottleEvents\",\"TableName\",\"",
              {
                "Ref": "HitsFF5AF8CD"
              },
              "\",{\"stat\":\"Sum\"}]],\"yAxis\":{}}}]}"
            ]
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "DynamoDBTable/CloudWatchDashBoard/Resource"
      }
    },
    "CDKMetadata": {
      "Type": "AWS::CDK::Metadata",
      "Properties": {
        "Analytics": "v2:deflate64:H4sIAAAAAAAA/0WMQQqDMBREz+I+fg1uumyxByi2F/gmEVM1H5IfRELu3qrQrmbmzTASZHOBurjiGkqlpyop8gbSk1FNojOBoldGtOQC+6hYtIP708F9C23Zkstif0h6c7iQ7iG9sJ+PyWGyUDNFvSKrEdJtRr/s3WnuGMae0Osd/ULOWTw2HslVDcgaZPEO1pY+OraLge7UD0qRV8rBAAAA"
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
    "ExportsOutputFnGetAttHitsFF5AF8CDArn18792E32": {
      "Value": {
        "Fn::GetAtt": [
          "HitsFF5AF8CD",
          "Arn"
        ]
      },
      "Export": {
        "Name": "DynamoDBTable:ExportsOutputFnGetAttHitsFF5AF8CDArn18792E32"
      }
    },
    "ExportsOutputRefHitsFF5AF8CDC54C3C7B": {
      "Value": {
        "Ref": "HitsFF5AF8CD"
      },
      "Export": {
        "Name": "DynamoDBTable:ExportsOutputRefHitsFF5AF8CDC54C3C7B"
      }
    }
  }
}
        )