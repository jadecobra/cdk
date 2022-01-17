from tests.utilities import TestTemplates, true, false


class TestLambdaFunction(TestTemplates):

    def test_lambda_function(self):
        self.assert_template_equal(
            'LambdaFunction',
            {
  "Resources": {
    "hitcounterErrorTopicB8385607": {
      "Type": "AWS::SNS::Topic",
      "Properties": {
        "DisplayName": "ErrorTopic"
      },
      "Metadata": {
        "aws:cdk:path": "LambdaFunction/hit_counter/ErrorTopic/Resource"
      }
    },
    "hitcounterawsxraysdkLambdaLayerC2C52DF3": {
      "Type": "AWS::Lambda::LayerVersion",
      "Properties": {
        "Content": {
          "S3Bucket": {
            "Ref": "AssetParametersd8a9de398a8d94394f523eb048f8c992b721ccd2294b3ae9f90cfc890e704b81S3BucketC7A2EC7F"
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
                          "Ref": "AssetParametersd8a9de398a8d94394f523eb048f8c992b721ccd2294b3ae9f90cfc890e704b81S3VersionKeyF23940AD"
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
                          "Ref": "AssetParametersd8a9de398a8d94394f523eb048f8c992b721ccd2294b3ae9f90cfc890e704b81S3VersionKeyF23940AD"
                        }
                      ]
                    }
                  ]
                }
              ]
            ]
          }
        },
        "Description": "AWS XRay SDK Lambda Layer"
      },
      "Metadata": {
        "aws:cdk:path": "LambdaFunction/hit_counter/aws-xray-sdkLambdaLayer/Resource",
        "aws:asset:path": "asset.d8a9de398a8d94394f523eb048f8c992b721ccd2294b3ae9f90cfc890e704b81",
        "aws:asset:is-bundled": false,
        "aws:asset:property": "Content"
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
        "aws:cdk:path": "LambdaFunction/hit_counter/LambdaFunction/ServiceRole/Resource"
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
                  "Fn::ImportValue": "DynamoDBTable:ExportsOutputFnGetAttHits9BF577DEArnFF8B7C1B"
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
        "aws:cdk:path": "LambdaFunction/hit_counter/LambdaFunction/ServiceRole/DefaultPolicy/Resource"
      }
    },
    "hitcounterLambdaFunctionB862C182": {
      "Type": "AWS::Lambda::Function",
      "Properties": {
        "Code": {
          "S3Bucket": {
            "Ref": "AssetParameters42961f7a43eb8def8a88d0711b3c95740379627ec280319af30490b76a248e16S3Bucket2E949244"
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
                          "Ref": "AssetParameters42961f7a43eb8def8a88d0711b3c95740379627ec280319af30490b76a248e16S3VersionKeyBF41F02A"
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
                          "Ref": "AssetParameters42961f7a43eb8def8a88d0711b3c95740379627ec280319af30490b76a248e16S3VersionKeyBF41F02A"
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
              "Fn::ImportValue": "DynamoDBTable:ExportsOutputRefHits9BF577DEBF202F48"
            }
          }
        },
        "Handler": "hit_counter.handler",
        "Layers": [
          {
            "Ref": "hitcounterawsxraysdkLambdaLayerC2C52DF3"
          }
        ],
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
        "aws:cdk:path": "LambdaFunction/hit_counter/LambdaFunction/Resource",
        "aws:asset:path": "asset.42961f7a43eb8def8a88d0711b3c95740379627ec280319af30490b76a248e16",
        "aws:asset:is-bundled": false,
        "aws:asset:property": "Code"
      }
    },
    "hitcounterLambdainvocationErrors2FEF99F1B": {
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
            "Expression": "(errors / invocations) * 100",
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
            "Id": "errors",
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
        "aws:cdk:path": "LambdaFunction/hit_counter/Lambda invocation Errors > 2%/Resource"
      }
    },
    "hitcounterLambdap99LongDuration1s890E8A7D": {
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
        "aws:cdk:path": "LambdaFunction/hit_counter/Lambda p99 Long Duration (>1s)/Resource"
      }
    },
    "hitcounterLambdaThrottledinvocations253B0DEB1": {
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
            "Expression": "(throttles * 100) / (invocations + throttles)",
            "Id": "expr_1",
            "Label": "throttled requests % in last 30 mins"
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
            "Id": "throttles",
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
        "aws:cdk:path": "LambdaFunction/hit_counter/Lambda Throttled invocations >2%/Resource"
      }
    },
    "hitcounterCloudWatchDashBoard56CA7346": {
      "Type": "AWS::CloudWatch::Dashboard",
      "Properties": {
        "DashboardBody": {
          "Fn::Join": [
            "",
            [
              "{\"widgets\":[{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":0,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Lambda Error %\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":false,\"metrics\":[[{\"label\":\"% of invocations that errored, last 5 mins\",\"expression\":\"(errors / invocations) * 100\"}],[\"AWS/Lambda\",\"Invocations\",\"FunctionName\",\"",
              {
                "Ref": "hitcounterLambdaFunctionB862C182"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"invocations\"}],[\"AWS/Lambda\",\"Errors\",\"FunctionName\",\"",
              {
                "Ref": "hitcounterLambdaFunctionB862C182"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"errors\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":6,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Lambda Duration\",\"region\":\"",
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
              "\",{\"stat\":\"p99\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":12,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Lambda Throttle %\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":false,\"metrics\":[[{\"label\":\"throttled requests % in last 30 mins\",\"expression\":\"(throttles * 100) / (invocations + throttles)\"}],[\"AWS/Lambda\",\"Invocations\",\"FunctionName\",\"",
              {
                "Ref": "hitcounterLambdaFunctionB862C182"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"invocations\"}],[\"AWS/Lambda\",\"Throttles\",\"FunctionName\",\"",
              {
                "Ref": "hitcounterLambdaFunctionB862C182"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"throttles\"}]],\"yAxis\":{}}}]}"
            ]
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "LambdaFunction/hit_counter/CloudWatchDashBoard/Resource"
      }
    },
    "CDKMetadata": {
      "Type": "AWS::CDK::Metadata",
      "Properties": {
        "Analytics": "v2:deflate64:H4sIAAAAAAAA/1WOQU/DMAyFf8vuqbeqJ25sQ5w4VAVx99ywhqYJih1NVZT/TpMBEid/7z3bei203QMcdo9444bGeZ/IBw3pVZBmdfaOJUQSdWTWsplX467q/OF6DLho0aGIQbOPgXTh7WQ0YrzLqrxM7BjSm/8yVNIKWVlcLiNCesFVh3cdeNsv8T/9HB3JT/DLWXHXYOnCUCttGk6RZi0nZK0MLpAGb2uVOntvDa21cqWsyPo43lBognS0GJYS3uEJebp4DGOx/kTOWfWrTN7tO2gP0O4+2ZgmRCdm0TDc5zdx/Ex1SgEAAA=="
      },
      "Metadata": {
        "aws:cdk:path": "LambdaFunction/CDKMetadata/Default"
      },
      "Condition": "CDKMetadataAvailable"
    }
  },
  "Parameters": {
    "AssetParametersd8a9de398a8d94394f523eb048f8c992b721ccd2294b3ae9f90cfc890e704b81S3BucketC7A2EC7F": {
      "Type": "String",
      "Description": "S3 bucket for asset \"d8a9de398a8d94394f523eb048f8c992b721ccd2294b3ae9f90cfc890e704b81\""
    },
    "AssetParametersd8a9de398a8d94394f523eb048f8c992b721ccd2294b3ae9f90cfc890e704b81S3VersionKeyF23940AD": {
      "Type": "String",
      "Description": "S3 key for asset version \"d8a9de398a8d94394f523eb048f8c992b721ccd2294b3ae9f90cfc890e704b81\""
    },
    "AssetParametersd8a9de398a8d94394f523eb048f8c992b721ccd2294b3ae9f90cfc890e704b81ArtifactHashA3AAFFE1": {
      "Type": "String",
      "Description": "Artifact hash for asset \"d8a9de398a8d94394f523eb048f8c992b721ccd2294b3ae9f90cfc890e704b81\""
    },
    "AssetParameters42961f7a43eb8def8a88d0711b3c95740379627ec280319af30490b76a248e16S3Bucket2E949244": {
      "Type": "String",
      "Description": "S3 bucket for asset \"42961f7a43eb8def8a88d0711b3c95740379627ec280319af30490b76a248e16\""
    },
    "AssetParameters42961f7a43eb8def8a88d0711b3c95740379627ec280319af30490b76a248e16S3VersionKeyBF41F02A": {
      "Type": "String",
      "Description": "S3 key for asset version \"42961f7a43eb8def8a88d0711b3c95740379627ec280319af30490b76a248e16\""
    },
    "AssetParameters42961f7a43eb8def8a88d0711b3c95740379627ec280319af30490b76a248e16ArtifactHashDDCB2305": {
      "Type": "String",
      "Description": "Artifact hash for asset \"42961f7a43eb8def8a88d0711b3c95740379627ec280319af30490b76a248e16\""
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
    "ExportsOutputFnGetAtthitcounterLambdaFunctionB862C182Arn3B74EE41": {
      "Value": {
        "Fn::GetAtt": [
          "hitcounterLambdaFunctionB862C182",
          "Arn"
        ]
      },
      "Export": {
        "Name": "LambdaFunction:ExportsOutputFnGetAtthitcounterLambdaFunctionB862C182Arn3B74EE41"
      }
    }
  }
}
        )