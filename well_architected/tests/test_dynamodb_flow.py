from tests.utilities import TestTemplates, true, false


class TestDynamoDBFlow(TestTemplates):

    def test_dynamodb_flow(self):
        self.assert_template_equal(
            'DynamoDBFlow',
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
        "ProvisionedThroughput": {
          "ReadCapacityUnits": 5,
          "WriteCapacityUnits": 5
        }
      },
      "UpdateReplacePolicy": "Retain",
      "DeletionPolicy": "Retain",
      "Metadata": {
        "aws:cdk:path": "DynamoDBFlow/Hits/Resource"
      }
    },
    "hitcounterErrorTopicB8385607": {
      "Type": "AWS::SNS::Topic",
      "Properties": {
        "DisplayName": "ErrorTopic",
        "TopicName": "ErrorTopic"
      },
      "Metadata": {
        "aws:cdk:path": "DynamoDBFlow/hit_counter/ErrorTopic/Resource"
      }
    },
    "hitcounterLambdaFunctionServiceRoleE2452AC5": {
      "Type": "AWS::IAM::Role",
      "Properties": {
        "AssumeRolePolicyDocument": {
          "Statement": [
            {
              "Action": "sts:AssumeRole",
              "Effect": "Allow",
              "Principal": {
                "Service": "lambda.amazonaws.com"
              }
            }
          ],
          "Version": "2012-10-17"
        },
        "ManagedPolicyArns": [
          {
            "Fn::Join": [
              "",
              [
                "arn:",
                {
                  "Ref": "AWS::Partition"
                },
                ":iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
              ]
            ]
          }
        ]
      },
      "Metadata": {
        "aws:cdk:path": "DynamoDBFlow/hit_counter/LambdaFunction/ServiceRole/Resource"
      }
    },
    "hitcounterLambdaFunctionServiceRoleDefaultPolicyBCDA98FD": {
      "Type": "AWS::IAM::Policy",
      "Properties": {
        "PolicyDocument": {
          "Statement": [
            {
              "Action": [
                "xray:PutTraceSegments",
                "xray:PutTelemetryRecords"
              ],
              "Effect": "Allow",
              "Resource": "*"
            },
            {
              "Action": [
                "dynamodb:BatchGetItem",
                "dynamodb:GetRecords",
                "dynamodb:GetShardIterator",
                "dynamodb:Query",
                "dynamodb:GetItem",
                "dynamodb:Scan",
                "dynamodb:ConditionCheckItem",
                "dynamodb:BatchWriteItem",
                "dynamodb:PutItem",
                "dynamodb:UpdateItem",
                "dynamodb:DeleteItem"
              ],
              "Effect": "Allow",
              "Resource": [
                {
                  "Fn::GetAtt": [
                    "HitsFF5AF8CD",
                    "Arn"
                  ]
                },
                {
                  "Ref": "AWS::NoValue"
                }
              ]
            }
          ],
          "Version": "2012-10-17"
        },
        "PolicyName": "hitcounterLambdaFunctionServiceRoleDefaultPolicyBCDA98FD",
        "Roles": [
          {
            "Ref": "hitcounterLambdaFunctionServiceRoleE2452AC5"
          }
        ]
      },
      "Metadata": {
        "aws:cdk:path": "DynamoDBFlow/hit_counter/LambdaFunction/ServiceRole/DefaultPolicy/Resource"
      }
    },
    "hitcounterLambdaFunctionB862C182": {
      "Type": "AWS::Lambda::Function",
      "Properties": {
        "Code": {
          "S3Bucket": {
            "Ref": "AssetParametersdbb5ee403884500d31ec6cd56022356492900e9a5847a21193393796cc85f66aS3BucketC8A66B57"
          },
          "S3Key": {
            "Fn::Join": [
              "",
              [
                {
                  "Fn::Select": [
                    0,
                    {
                      "Fn::Split": [
                        "||",
                        {
                          "Ref": "AssetParametersdbb5ee403884500d31ec6cd56022356492900e9a5847a21193393796cc85f66aS3VersionKeyDBAE7B4A"
                        }
                      ]
                    }
                  ]
                },
                {
                  "Fn::Select": [
                    1,
                    {
                      "Fn::Split": [
                        "||",
                        {
                          "Ref": "AssetParametersdbb5ee403884500d31ec6cd56022356492900e9a5847a21193393796cc85f66aS3VersionKeyDBAE7B4A"
                        }
                      ]
                    }
                  ]
                }
              ]
            ]
          }
        },
        "Role": {
          "Fn::GetAtt": [
            "hitcounterLambdaFunctionServiceRoleE2452AC5",
            "Arn"
          ]
        },
        "Environment": {
          "Variables": {
            "HITS_TABLE_NAME": {
              "Ref": "HitsFF5AF8CD"
            }
          }
        },
        "Handler": "hit_counter.handler",
        "Runtime": "python3.8",
        "Timeout": 60,
        "TracingConfig": {
          "Mode": "Active"
        }
      },
      "DependsOn": [
        "hitcounterLambdaFunctionServiceRoleDefaultPolicyBCDA98FD",
        "hitcounterLambdaFunctionServiceRoleE2452AC5"
      ],
      "Metadata": {
        "aws:cdk:path": "DynamoDBFlow/hit_counter/LambdaFunction/Resource",
        "aws:asset:path": "asset.dbb5ee403884500d31ec6cd56022356492900e9a5847a21193393796cc85f66a",
        "aws:asset:is-bundled": false,
        "aws:asset:property": "Code"
      }
    },
    "hitcounterLambdaFunctionAllowInvokeXRayTracerSnsFanOutTopic4E706A091FB77B96": {
      "Type": "AWS::Lambda::Permission",
      "Properties": {
        "Action": "lambda:InvokeFunction",
        "FunctionName": {
          "Fn::GetAtt": [
            "hitcounterLambdaFunctionB862C182",
            "Arn"
          ]
        },
        "Principal": "sns.amazonaws.com",
        "SourceArn": {
          "Fn::ImportValue": "XRayTracerSnsFanOutTopic:ExportsOutputRefXRayTracerSnsFanOutTopic129D23A131FFD088"
        }
      },
      "Metadata": {
        "aws:cdk:path": "DynamoDBFlow/hit_counter/LambdaFunction/AllowInvoke:XRayTracerSnsFanOutTopic4E706A09"
      }
    },
    "hitcounterLambdaFunctionXRayTracerSnsFanOutTopicAFE0C45F": {
      "Type": "AWS::SNS::Subscription",
      "Properties": {
        "Protocol": "lambda",
        "TopicArn": {
          "Fn::ImportValue": "XRayTracerSnsFanOutTopic:ExportsOutputRefXRayTracerSnsFanOutTopic129D23A131FFD088"
        },
        "Endpoint": {
          "Fn::GetAtt": [
            "hitcounterLambdaFunctionB862C182",
            "Arn"
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "DynamoDBFlow/hit_counter/LambdaFunction/XRayTracerSnsFanOutTopic/Resource"
      }
    },
    "hitcounterDynamoLambda2Error497B073E": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "hitcounterErrorTopicB8385607"
          }
        ],
        "DatapointsToAlarm": 1,
        "Metrics": [
          {
            "Expression": "e / invocations * 100",
            "Id": "expr_1",
            "Label": "% of invocations that errored, last 5 mins"
          },
          {
            "Id": "invocations",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "FunctionName",
                    "Value": {
                      "Ref": "hitcounterLambdaFunctionB862C182"
                    }
                  }
                ],
                "MetricName": "Invocations",
                "Namespace": "AWS/Lambda"
              },
              "Period": 300,
              "Stat": "Sum"
            },
            "ReturnData": false
          },
          {
            "Id": "e",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "FunctionName",
                    "Value": {
                      "Ref": "hitcounterLambdaFunctionB862C182"
                    }
                  }
                ],
                "MetricName": "Errors",
                "Namespace": "AWS/Lambda"
              },
              "Period": 300,
              "Stat": "Sum"
            },
            "ReturnData": false
          }
        ],
        "Threshold": 2,
        "TreatMissingData": "notBreaching"
      },
      "Metadata": {
        "aws:cdk:path": "DynamoDBFlow/hit_counter/Dynamo Lambda 2% Error/Resource"
      }
    },
    "hitcounterDynamoLambdap99LongDuration1s6366F631": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "hitcounterErrorTopicB8385607"
          }
        ],
        "DatapointsToAlarm": 1,
        "Dimensions": [
          {
            "Name": "FunctionName",
            "Value": {
              "Ref": "hitcounterLambdaFunctionB862C182"
            }
          }
        ],
        "ExtendedStatistic": "p99",
        "MetricName": "Duration",
        "Namespace": "AWS/Lambda",
        "Period": 300,
        "Threshold": 1000,
        "TreatMissingData": "notBreaching"
      },
      "Metadata": {
        "aws:cdk:path": "DynamoDBFlow/hit_counter/Dynamo Lambda p99 Long Duration (>1s)/Resource"
      }
    },
    "hitcounterDynamoLambda2Throttled25E14661": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "hitcounterErrorTopicB8385607"
          }
        ],
        "DatapointsToAlarm": 1,
        "Metrics": [
          {
            "Expression": "t / (invocations + t) * 100",
            "Id": "expr_1",
            "Label": "% of throttled requests, last 30 mins"
          },
          {
            "Id": "invocations",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "FunctionName",
                    "Value": {
                      "Ref": "hitcounterLambdaFunctionB862C182"
                    }
                  }
                ],
                "MetricName": "Invocations",
                "Namespace": "AWS/Lambda"
              },
              "Period": 300,
              "Stat": "Sum"
            },
            "ReturnData": false
          },
          {
            "Id": "t",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "FunctionName",
                    "Value": {
                      "Ref": "hitcounterLambdaFunctionB862C182"
                    }
                  }
                ],
                "MetricName": "Throttles",
                "Namespace": "AWS/Lambda"
              },
              "Period": 300,
              "Stat": "Sum"
            },
            "ReturnData": false
          }
        ],
        "Threshold": 2,
        "TreatMissingData": "notBreaching"
      },
      "Metadata": {
        "aws:cdk:path": "DynamoDBFlow/hit_counter/Dynamo Lambda 2% Throttled/Resource"
      }
    },
    "hitcounterCloudWatchDashBoard56CA7346": {
      "Type": "AWS::CloudWatch::Dashboard",
      "Properties": {
        "DashboardBody": {
          "Fn::Join": [
            "",
            [
              "{\"widgets\":[{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":0,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Dynamo Lambda Error %\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":false,\"metrics\":[[{\"label\":\"% of invocations that errored, last 5 mins\",\"expression\":\"e / invocations * 100\"}],[\"AWS/Lambda\",\"Invocations\",\"FunctionName\",\"",
              {
                "Ref": "hitcounterLambdaFunctionB862C182"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"invocations\"}],[\"AWS/Lambda\",\"Errors\",\"FunctionName\",\"",
              {
                "Ref": "hitcounterLambdaFunctionB862C182"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"e\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":6,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Dynamo Lambda Duration\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":true,\"metrics\":[[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "hitcounterLambdaFunctionB862C182"
              },
              "\",{\"stat\":\"p50\"}],[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "hitcounterLambdaFunctionB862C182"
              },
              "\",{\"stat\":\"p90\"}],[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "hitcounterLambdaFunctionB862C182"
              },
              "\",{\"stat\":\"p99\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":12,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Dynamo Lambda Throttle %\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":false,\"metrics\":[[{\"label\":\"% of throttled requests, last 30 mins\",\"expression\":\"t / (invocations + t) * 100\"}],[\"AWS/Lambda\",\"Invocations\",\"FunctionName\",\"",
              {
                "Ref": "hitcounterLambdaFunctionB862C182"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"invocations\"}],[\"AWS/Lambda\",\"Throttles\",\"FunctionName\",\"",
              {
                "Ref": "hitcounterLambdaFunctionB862C182"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"t\"}]],\"yAxis\":{}}}]}"
            ]
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "DynamoDBFlow/hit_counter/CloudWatchDashBoard/Resource"
      }
    },
    "CDKMetadata": {
      "Type": "AWS::CDK::Metadata",
      "Properties": {
        "Analytics": "v2:deflate64:H4sIAAAAAAAA/02PwW7DIAyGn6V34jbKabe1nXaO0r2AY2jDGqDCoCpCvPsC0bae/P8/n23cQtu9wWH3jk9uSN73iZxXkC4B6S4GxS56UuLsLAcfKYgjswrr603bmzhfbY8ejQrKF/PPX+3aInXQzmZRZie5WDROjpC+cJwrUkUWbHkN3UNTDau4xJHJ60cZUNJXn8WMZpQI6TNa+iVeda+80cyV1WggDW7bWGvvZk1L5apaf9A1WO5iqOetHk6R7iqckJWg2UX5xEATpOOM3pTWTXwgT6NDL0v0Z3LOol/C5Oy+g/YA7e6btW58tEEbBcNWfwCZsC+6ewEAAA=="
      },
      "Metadata": {
        "aws:cdk:path": "DynamoDBFlow/CDKMetadata/Default"
      },
      "Condition": "CDKMetadataAvailable"
    }
  },
  "Parameters": {
    "AssetParametersdbb5ee403884500d31ec6cd56022356492900e9a5847a21193393796cc85f66aS3BucketC8A66B57": {
      "Type": "String",
      "Description": "S3 bucket for asset \"dbb5ee403884500d31ec6cd56022356492900e9a5847a21193393796cc85f66a\""
    },
    "AssetParametersdbb5ee403884500d31ec6cd56022356492900e9a5847a21193393796cc85f66aS3VersionKeyDBAE7B4A": {
      "Type": "String",
      "Description": "S3 key for asset version \"dbb5ee403884500d31ec6cd56022356492900e9a5847a21193393796cc85f66a\""
    },
    "AssetParametersdbb5ee403884500d31ec6cd56022356492900e9a5847a21193393796cc85f66aArtifactHash62B09B39": {
      "Type": "String",
      "Description": "Artifact hash for asset \"dbb5ee403884500d31ec6cd56022356492900e9a5847a21193393796cc85f66a\""
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
  }
}
        )