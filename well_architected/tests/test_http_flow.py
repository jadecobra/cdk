from tests.utilities import TestTemplates, true, false


class TestHttpFlow(TestTemplates):

    def test_http_flow(self):
        self.assert_template_equal(
            'HttpFlow',
            {
  "Resources": {
    "httpErrorTopic874FB9D4": {
      "Type": "AWS::SNS::Topic",
      "Properties": {
        "DisplayName": "ErrorTopic"
      },
      "Metadata": {
        "aws:cdk:path": "HttpFlow/http/ErrorTopic/Resource"
      }
    },
    "httpawsxraysdkLambdaLayer26FEA83F": {
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
        "aws:cdk:path": "HttpFlow/http/aws-xray-sdkLambdaLayer/Resource",
        "aws:asset:path": "asset.d8a9de398a8d94394f523eb048f8c992b721ccd2294b3ae9f90cfc890e704b81",
        "aws:asset:is-bundled": false,
        "aws:asset:property": "Content"
      }
    },
    "httpLambdaFunctionServiceRoleBB063197": {
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
        "aws:cdk:path": "HttpFlow/http/LambdaFunction/ServiceRole/Resource"
      }
    },
    "httpLambdaFunctionServiceRoleDefaultPolicy5FD0C40D": {
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
            }
          ],
          "Version": "2012-10-17"
        },
        "PolicyName": "httpLambdaFunctionServiceRoleDefaultPolicy5FD0C40D",
        "Roles": [
          {
            "Ref": "httpLambdaFunctionServiceRoleBB063197"
          }
        ]
      },
      "Metadata": {
        "aws:cdk:path": "HttpFlow/http/LambdaFunction/ServiceRole/DefaultPolicy/Resource"
      }
    },
    "httpLambdaFunction9ED72A36": {
      "Type": "AWS::Lambda::Function",
      "Properties": {
        "Code": {
          "S3Bucket": {
            "Ref": "AssetParameters32986536b3b46945ee3c22f84dda5e537c348c3a6a55627c6477eb9d16c5c0bdS3Bucket60C4924F"
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
                          "Ref": "AssetParameters32986536b3b46945ee3c22f84dda5e537c348c3a6a55627c6477eb9d16c5c0bdS3VersionKey6E81F61A"
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
                          "Ref": "AssetParameters32986536b3b46945ee3c22f84dda5e537c348c3a6a55627c6477eb9d16c5c0bdS3VersionKey6E81F61A"
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
            "httpLambdaFunctionServiceRoleBB063197",
            "Arn"
          ]
        },
        "Handler": "http.handler",
        "Layers": [
          {
            "Ref": "httpawsxraysdkLambdaLayer26FEA83F"
          }
        ],
        "Runtime": "python3.8",
        "Timeout": 60,
        "TracingConfig": {
          "Mode": "Active"
        }
      },
      "DependsOn": [
        "httpLambdaFunctionServiceRoleDefaultPolicy5FD0C40D",
        "httpLambdaFunctionServiceRoleBB063197"
      ],
      "Metadata": {
        "aws:cdk:path": "HttpFlow/http/LambdaFunction/Resource",
        "aws:asset:path": "asset.32986536b3b46945ee3c22f84dda5e537c348c3a6a55627c6477eb9d16c5c0bd",
        "aws:asset:is-bundled": false,
        "aws:asset:property": "Code"
      }
    },
    "httpLambdaFunctionAllowInvokeXRayTracerSnsFanOutTopic4E706A09F3311B40": {
      "Type": "AWS::Lambda::Permission",
      "Properties": {
        "Action": "lambda:InvokeFunction",
        "FunctionName": {
          "Fn::GetAtt": [
            "httpLambdaFunction9ED72A36",
            "Arn"
          ]
        },
        "Principal": "sns.amazonaws.com",
        "SourceArn": {
          "Fn::ImportValue": "XRayTracerSnsFanOutTopic:ExportsOutputRefXRayTracerSnsFanOutTopic129D23A131FFD088"
        }
      },
      "Metadata": {
        "aws:cdk:path": "HttpFlow/http/LambdaFunction/AllowInvoke:XRayTracerSnsFanOutTopic4E706A09"
      }
    },
    "httpLambdaFunctionXRayTracerSnsFanOutTopic38CFBD2A": {
      "Type": "AWS::SNS::Subscription",
      "Properties": {
        "Protocol": "lambda",
        "TopicArn": {
          "Fn::ImportValue": "XRayTracerSnsFanOutTopic:ExportsOutputRefXRayTracerSnsFanOutTopic129D23A131FFD088"
        },
        "Endpoint": {
          "Fn::GetAtt": [
            "httpLambdaFunction9ED72A36",
            "Arn"
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "HttpFlow/http/LambdaFunction/XRayTracerSnsFanOutTopic/Resource"
      }
    },
    "httpLambdainvocationErrors2490F7C4F": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "httpErrorTopic874FB9D4"
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
                      "Ref": "httpLambdaFunction9ED72A36"
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
                      "Ref": "httpLambdaFunction9ED72A36"
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
        "aws:cdk:path": "HttpFlow/http/Lambda invocation Errors > 2%/Resource"
      }
    },
    "httpLambdap99LongDuration1sCFCABB7C": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "httpErrorTopic874FB9D4"
          }
        ],
        "DatapointsToAlarm": 1,
        "Dimensions": [
          {
            "Name": "FunctionName",
            "Value": {
              "Ref": "httpLambdaFunction9ED72A36"
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
        "aws:cdk:path": "HttpFlow/http/Lambda p99 Long Duration (>1s)/Resource"
      }
    },
    "httpLambdaThrottledinvocations203A2EC64": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "httpErrorTopic874FB9D4"
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
                      "Ref": "httpLambdaFunction9ED72A36"
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
                      "Ref": "httpLambdaFunction9ED72A36"
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
        "aws:cdk:path": "HttpFlow/http/Lambda Throttled invocations >2%/Resource"
      }
    },
    "httpCloudWatchDashBoard87A3CD2A": {
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
                "Ref": "httpLambdaFunction9ED72A36"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"invocations\"}],[\"AWS/Lambda\",\"Errors\",\"FunctionName\",\"",
              {
                "Ref": "httpLambdaFunction9ED72A36"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"errors\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":6,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Lambda Duration\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":true,\"metrics\":[[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "httpLambdaFunction9ED72A36"
              },
              "\",{\"stat\":\"p50\"}],[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "httpLambdaFunction9ED72A36"
              },
              "\",{\"stat\":\"p90\"}],[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "httpLambdaFunction9ED72A36"
              },
              "\",{\"stat\":\"p99\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":12,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Lambda Throttle %\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":false,\"metrics\":[[{\"label\":\"throttled requests % in last 30 mins\",\"expression\":\"(throttles * 100) / (invocations + throttles)\"}],[\"AWS/Lambda\",\"Invocations\",\"FunctionName\",\"",
              {
                "Ref": "httpLambdaFunction9ED72A36"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"invocations\"}],[\"AWS/Lambda\",\"Throttles\",\"FunctionName\",\"",
              {
                "Ref": "httpLambdaFunction9ED72A36"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"throttles\"}]],\"yAxis\":{}}}]}"
            ]
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "HttpFlow/http/CloudWatchDashBoard/Resource"
      }
    },
    "CDKMetadata": {
      "Type": "AWS::CDK::Metadata",
      "Properties": {
        "Analytics": "v2:deflate64:H4sIAAAAAAAA/1WOsW7DMAxEvyW7zMTw1K1Jik4dDKfoTstsrNqSAlFCYAj691pyW6QT7x3Jw9VQN09w2D3jnSs5TPsorSOIF49yEmdr2LsgvTgyk1/NqzJXcf40LTrU5Mll6IhtcJKyXl8G5ZU1SeTIyIYhvtubknm7iUvoWTp1y2fZfeQkZtT9gBDfcCH3QY5/rv7xazDy9/1Rt+S0Yi5B3FSYazOU9ivDKciJ/AmZhEINsbNzaV1ma2cll5JSVBJytmG4o5cjxOOMTuflJl6Qx96iG7L1Bykl0S5+tGbfQH2AevfFSlUuGK80QbfNb2OjuiF1AQAA"
      },
      "Metadata": {
        "aws:cdk:path": "HttpFlow/CDKMetadata/Default"
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
    "AssetParameters32986536b3b46945ee3c22f84dda5e537c348c3a6a55627c6477eb9d16c5c0bdS3Bucket60C4924F": {
      "Type": "String",
      "Description": "S3 bucket for asset \"32986536b3b46945ee3c22f84dda5e537c348c3a6a55627c6477eb9d16c5c0bd\""
    },
    "AssetParameters32986536b3b46945ee3c22f84dda5e537c348c3a6a55627c6477eb9d16c5c0bdS3VersionKey6E81F61A": {
      "Type": "String",
      "Description": "S3 key for asset version \"32986536b3b46945ee3c22f84dda5e537c348c3a6a55627c6477eb9d16c5c0bd\""
    },
    "AssetParameters32986536b3b46945ee3c22f84dda5e537c348c3a6a55627c6477eb9d16c5c0bdArtifactHash97D2A9D2": {
      "Type": "String",
      "Description": "Artifact hash for asset \"32986536b3b46945ee3c22f84dda5e537c348c3a6a55627c6477eb9d16c5c0bd\""
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