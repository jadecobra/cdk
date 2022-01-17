from tests.utilities import TestTemplates, true, false


class TestSnsFlow(TestTemplates):

    def test_sns_flow(self):
        self.assert_template_equal(
            'SnsFlow',
            {
  "Resources": {
    "TheXRayTracerSnsTopicCCE2005E": {
      "Type": "AWS::SNS::Topic",
      "Properties": {
        "DisplayName": "The XRay Tracer CDK Pattern Topic"
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/TheXRayTracerSnsTopic/Resource"
      }
    },
    "snspublishErrorTopic167BD513": {
      "Type": "AWS::SNS::Topic",
      "Properties": {
        "DisplayName": "ErrorTopic"
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_publish/ErrorTopic/Resource"
      }
    },
    "snspublishawsxraysdkLambdaLayer2E8A5647": {
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
        "aws:cdk:path": "SnsFlow/sns_publish/aws-xray-sdkLambdaLayer/Resource",
        "aws:asset:path": "asset.d8a9de398a8d94394f523eb048f8c992b721ccd2294b3ae9f90cfc890e704b81",
        "aws:asset:is-bundled": false,
        "aws:asset:property": "Content"
      }
    },
    "snspublishLambdaFunctionServiceRoleBE8DA9C2": {
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
        "aws:cdk:path": "SnsFlow/sns_publish/LambdaFunction/ServiceRole/Resource"
      }
    },
    "snspublishLambdaFunctionServiceRoleDefaultPolicyD927DA99": {
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
              "Action": "sns:Publish",
              "Effect": "Allow",
              "Resource": {
                "Ref": "TheXRayTracerSnsTopicCCE2005E"
              }
            }
          ],
          "Version": "2012-10-17"
        },
        "PolicyName": "snspublishLambdaFunctionServiceRoleDefaultPolicyD927DA99",
        "Roles": [
          {
            "Ref": "snspublishLambdaFunctionServiceRoleBE8DA9C2"
          }
        ]
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_publish/LambdaFunction/ServiceRole/DefaultPolicy/Resource"
      }
    },
    "snspublishLambdaFunctionE7ECD8FF": {
      "Type": "AWS::Lambda::Function",
      "Properties": {
        "Code": {
          "S3Bucket": {
            "Ref": "AssetParametersef7aa034d437b1c1976e69f919345dcddf4b4c9c6a6947d000d52902c30271cfS3Bucket81A6DB81"
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
                          "Ref": "AssetParametersef7aa034d437b1c1976e69f919345dcddf4b4c9c6a6947d000d52902c30271cfS3VersionKey99E114A0"
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
                          "Ref": "AssetParametersef7aa034d437b1c1976e69f919345dcddf4b4c9c6a6947d000d52902c30271cfS3VersionKey99E114A0"
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
            "snspublishLambdaFunctionServiceRoleBE8DA9C2",
            "Arn"
          ]
        },
        "Environment": {
          "Variables": {
            "TOPIC_ARN": {
              "Ref": "TheXRayTracerSnsTopicCCE2005E"
            }
          }
        },
        "Handler": "sns_publish.handler",
        "Layers": [
          {
            "Ref": "snspublishawsxraysdkLambdaLayer2E8A5647"
          }
        ],
        "Runtime": "python3.8",
        "Timeout": 60,
        "TracingConfig": {
          "Mode": "Active"
        }
      },
      "DependsOn": [
        "snspublishLambdaFunctionServiceRoleDefaultPolicyD927DA99",
        "snspublishLambdaFunctionServiceRoleBE8DA9C2"
      ],
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_publish/LambdaFunction/Resource",
        "aws:asset:path": "asset.ef7aa034d437b1c1976e69f919345dcddf4b4c9c6a6947d000d52902c30271cf",
        "aws:asset:is-bundled": false,
        "aws:asset:property": "Code"
      }
    },
    "snspublishLambdaFunctionAllowInvokeSnsFlowSNSTopicACE071C85E8FF116": {
      "Type": "AWS::Lambda::Permission",
      "Properties": {
        "Action": "lambda:InvokeFunction",
        "FunctionName": {
          "Fn::GetAtt": [
            "snspublishLambdaFunctionE7ECD8FF",
            "Arn"
          ]
        },
        "Principal": "sns.amazonaws.com",
        "SourceArn": {
          "Fn::ImportValue": "XRayTracerSnsFanOutTopic:ExportsOutputRefXRayTracerSnsFanOutTopic129D23A131FFD088"
        }
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_publish/LambdaFunction/AllowInvoke:SnsFlowSNSTopicACE071C8"
      }
    },
    "snspublishLambdaFunctionSNSTopic766E3B5D": {
      "Type": "AWS::SNS::Subscription",
      "Properties": {
        "Protocol": "lambda",
        "TopicArn": {
          "Fn::ImportValue": "XRayTracerSnsFanOutTopic:ExportsOutputRefXRayTracerSnsFanOutTopic129D23A131FFD088"
        },
        "Endpoint": {
          "Fn::GetAtt": [
            "snspublishLambdaFunctionE7ECD8FF",
            "Arn"
          ]
        },
        "Region": {
          "Fn::Select": [
            3,
            {
              "Fn::Split": [
                ":",
                {
                  "Fn::ImportValue": "XRayTracerSnsFanOutTopic:ExportsOutputRefXRayTracerSnsFanOutTopic129D23A131FFD088"
                }
              ]
            }
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_publish/LambdaFunction/SNSTopic/Resource"
      }
    },
    "snspublishLambdainvocationErrors2194CE9F8": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "snspublishErrorTopic167BD513"
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
                      "Ref": "snspublishLambdaFunctionE7ECD8FF"
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
                      "Ref": "snspublishLambdaFunctionE7ECD8FF"
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
        "aws:cdk:path": "SnsFlow/sns_publish/Lambda invocation Errors > 2%/Resource"
      }
    },
    "snspublishLambdap99LongDuration1s0547A3C8": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "snspublishErrorTopic167BD513"
          }
        ],
        "DatapointsToAlarm": 1,
        "Dimensions": [
          {
            "Name": "FunctionName",
            "Value": {
              "Ref": "snspublishLambdaFunctionE7ECD8FF"
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
        "aws:cdk:path": "SnsFlow/sns_publish/Lambda p99 Long Duration (>1s)/Resource"
      }
    },
    "snspublishLambdaThrottledinvocations22BAA7401": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "snspublishErrorTopic167BD513"
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
                      "Ref": "snspublishLambdaFunctionE7ECD8FF"
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
                      "Ref": "snspublishLambdaFunctionE7ECD8FF"
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
        "aws:cdk:path": "SnsFlow/sns_publish/Lambda Throttled invocations >2%/Resource"
      }
    },
    "snspublishCloudWatchDashBoard5DA9CB77": {
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
                "Ref": "snspublishLambdaFunctionE7ECD8FF"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"invocations\"}],[\"AWS/Lambda\",\"Errors\",\"FunctionName\",\"",
              {
                "Ref": "snspublishLambdaFunctionE7ECD8FF"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"errors\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":6,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Lambda Duration\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":true,\"metrics\":[[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "snspublishLambdaFunctionE7ECD8FF"
              },
              "\",{\"stat\":\"p50\"}],[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "snspublishLambdaFunctionE7ECD8FF"
              },
              "\",{\"stat\":\"p90\"}],[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "snspublishLambdaFunctionE7ECD8FF"
              },
              "\",{\"stat\":\"p99\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":12,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Lambda Throttle %\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":false,\"metrics\":[[{\"label\":\"throttled requests % in last 30 mins\",\"expression\":\"(throttles * 100) / (invocations + throttles)\"}],[\"AWS/Lambda\",\"Invocations\",\"FunctionName\",\"",
              {
                "Ref": "snspublishLambdaFunctionE7ECD8FF"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"invocations\"}],[\"AWS/Lambda\",\"Throttles\",\"FunctionName\",\"",
              {
                "Ref": "snspublishLambdaFunctionE7ECD8FF"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"throttles\"}]],\"yAxis\":{}}}]}"
            ]
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_publish/CloudWatchDashBoard/Resource"
      }
    },
    "snssubscribeErrorTopicB1BEEA4E": {
      "Type": "AWS::SNS::Topic",
      "Properties": {
        "DisplayName": "ErrorTopic"
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_subscribe/ErrorTopic/Resource"
      }
    },
    "snssubscribeawsxraysdkLambdaLayerFB9F9B45": {
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
        "aws:cdk:path": "SnsFlow/sns_subscribe/aws-xray-sdkLambdaLayer/Resource",
        "aws:asset:path": "asset.d8a9de398a8d94394f523eb048f8c992b721ccd2294b3ae9f90cfc890e704b81",
        "aws:asset:is-bundled": false,
        "aws:asset:property": "Content"
      }
    },
    "snssubscribeLambdaFunctionServiceRole6068C33F": {
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
        "aws:cdk:path": "SnsFlow/sns_subscribe/LambdaFunction/ServiceRole/Resource"
      }
    },
    "snssubscribeLambdaFunctionServiceRoleDefaultPolicy7C3E54A8": {
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
        "PolicyName": "snssubscribeLambdaFunctionServiceRoleDefaultPolicy7C3E54A8",
        "Roles": [
          {
            "Ref": "snssubscribeLambdaFunctionServiceRole6068C33F"
          }
        ]
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_subscribe/LambdaFunction/ServiceRole/DefaultPolicy/Resource"
      }
    },
    "snssubscribeLambdaFunctionE84E36B6": {
      "Type": "AWS::Lambda::Function",
      "Properties": {
        "Code": {
          "S3Bucket": {
            "Ref": "AssetParameters974996a9096d42156ceb01e12ea154d428b9b643131593d6d5dbc4dc9d11918fS3Bucket69F99350"
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
                          "Ref": "AssetParameters974996a9096d42156ceb01e12ea154d428b9b643131593d6d5dbc4dc9d11918fS3VersionKey160115D9"
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
                          "Ref": "AssetParameters974996a9096d42156ceb01e12ea154d428b9b643131593d6d5dbc4dc9d11918fS3VersionKey160115D9"
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
            "snssubscribeLambdaFunctionServiceRole6068C33F",
            "Arn"
          ]
        },
        "Handler": "sns_subscribe.handler",
        "Layers": [
          {
            "Ref": "snssubscribeawsxraysdkLambdaLayerFB9F9B45"
          }
        ],
        "Runtime": "python3.8",
        "Timeout": 60,
        "TracingConfig": {
          "Mode": "Active"
        }
      },
      "DependsOn": [
        "snssubscribeLambdaFunctionServiceRoleDefaultPolicy7C3E54A8",
        "snssubscribeLambdaFunctionServiceRole6068C33F"
      ],
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_subscribe/LambdaFunction/Resource",
        "aws:asset:path": "asset.974996a9096d42156ceb01e12ea154d428b9b643131593d6d5dbc4dc9d11918f",
        "aws:asset:is-bundled": false,
        "aws:asset:property": "Code"
      }
    },
    "snssubscribeLambdaFunctionAllowInvokeSnsFlowTheXRayTracerSnsTopic2E3ECD150E3B6B47": {
      "Type": "AWS::Lambda::Permission",
      "Properties": {
        "Action": "lambda:InvokeFunction",
        "FunctionName": {
          "Fn::GetAtt": [
            "snssubscribeLambdaFunctionE84E36B6",
            "Arn"
          ]
        },
        "Principal": "sns.amazonaws.com",
        "SourceArn": {
          "Ref": "TheXRayTracerSnsTopicCCE2005E"
        }
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_subscribe/LambdaFunction/AllowInvoke:SnsFlowTheXRayTracerSnsTopic2E3ECD15"
      }
    },
    "snssubscribeLambdaFunctionTheXRayTracerSnsTopicC8EDB3DC": {
      "Type": "AWS::SNS::Subscription",
      "Properties": {
        "Protocol": "lambda",
        "TopicArn": {
          "Ref": "TheXRayTracerSnsTopicCCE2005E"
        },
        "Endpoint": {
          "Fn::GetAtt": [
            "snssubscribeLambdaFunctionE84E36B6",
            "Arn"
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_subscribe/LambdaFunction/TheXRayTracerSnsTopic/Resource"
      }
    },
    "snssubscribeLambdainvocationErrors2AA7BE787": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "snssubscribeErrorTopicB1BEEA4E"
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
                      "Ref": "snssubscribeLambdaFunctionE84E36B6"
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
                      "Ref": "snssubscribeLambdaFunctionE84E36B6"
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
        "aws:cdk:path": "SnsFlow/sns_subscribe/Lambda invocation Errors > 2%/Resource"
      }
    },
    "snssubscribeLambdap99LongDuration1s207F8DA0": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "snssubscribeErrorTopicB1BEEA4E"
          }
        ],
        "DatapointsToAlarm": 1,
        "Dimensions": [
          {
            "Name": "FunctionName",
            "Value": {
              "Ref": "snssubscribeLambdaFunctionE84E36B6"
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
        "aws:cdk:path": "SnsFlow/sns_subscribe/Lambda p99 Long Duration (>1s)/Resource"
      }
    },
    "snssubscribeLambdaThrottledinvocations2104FA145": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "snssubscribeErrorTopicB1BEEA4E"
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
                      "Ref": "snssubscribeLambdaFunctionE84E36B6"
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
                      "Ref": "snssubscribeLambdaFunctionE84E36B6"
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
        "aws:cdk:path": "SnsFlow/sns_subscribe/Lambda Throttled invocations >2%/Resource"
      }
    },
    "snssubscribeCloudWatchDashBoard0367AF74": {
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
                "Ref": "snssubscribeLambdaFunctionE84E36B6"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"invocations\"}],[\"AWS/Lambda\",\"Errors\",\"FunctionName\",\"",
              {
                "Ref": "snssubscribeLambdaFunctionE84E36B6"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"errors\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":6,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Lambda Duration\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":true,\"metrics\":[[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "snssubscribeLambdaFunctionE84E36B6"
              },
              "\",{\"stat\":\"p50\"}],[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "snssubscribeLambdaFunctionE84E36B6"
              },
              "\",{\"stat\":\"p90\"}],[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "snssubscribeLambdaFunctionE84E36B6"
              },
              "\",{\"stat\":\"p99\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":12,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Lambda Throttle %\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":false,\"metrics\":[[{\"label\":\"throttled requests % in last 30 mins\",\"expression\":\"(throttles * 100) / (invocations + throttles)\"}],[\"AWS/Lambda\",\"Invocations\",\"FunctionName\",\"",
              {
                "Ref": "snssubscribeLambdaFunctionE84E36B6"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"invocations\"}],[\"AWS/Lambda\",\"Throttles\",\"FunctionName\",\"",
              {
                "Ref": "snssubscribeLambdaFunctionE84E36B6"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"throttles\"}]],\"yAxis\":{}}}]}"
            ]
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/sns_subscribe/CloudWatchDashBoard/Resource"
      }
    },
    "CDKMetadata": {
      "Type": "AWS::CDK::Metadata",
      "Properties": {
        "Analytics": "v2:deflate64:H4sIAAAAAAAA/1VPMW7DMAx8S3aZieGpW5MUnToYTtGdltlYtSUFooTAEPT3WnJbNBPvjscjWUPdPMFh94x3ruQw7aO0jiBePMpJnK1h74L04shMfhWvylzF+dO06FCTJ5dJR2yDk5TxOjIor6xJIkdGNgzx3d6UzN0NXELP0qlbtmX1gRfLCZmSmFH3A0J8w4XcBzn+8T/w12Dkb9B/3JLTirlcwk2F+QGG8sfK4RTkRD7vEQo1xM7O5f5SWzsruZSUgpKQsw3DHb0cIR5ndDo3N/CCPPYW3ZClP5JSEu3iR2v2DdQHqHdfrFTlgvFKE3Rb/QZ4CXn5fwEAAA=="
      },
      "Metadata": {
        "aws:cdk:path": "SnsFlow/CDKMetadata/Default"
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
    "AssetParametersef7aa034d437b1c1976e69f919345dcddf4b4c9c6a6947d000d52902c30271cfS3Bucket81A6DB81": {
      "Type": "String",
      "Description": "S3 bucket for asset \"ef7aa034d437b1c1976e69f919345dcddf4b4c9c6a6947d000d52902c30271cf\""
    },
    "AssetParametersef7aa034d437b1c1976e69f919345dcddf4b4c9c6a6947d000d52902c30271cfS3VersionKey99E114A0": {
      "Type": "String",
      "Description": "S3 key for asset version \"ef7aa034d437b1c1976e69f919345dcddf4b4c9c6a6947d000d52902c30271cf\""
    },
    "AssetParametersef7aa034d437b1c1976e69f919345dcddf4b4c9c6a6947d000d52902c30271cfArtifactHashD148D3CB": {
      "Type": "String",
      "Description": "Artifact hash for asset \"ef7aa034d437b1c1976e69f919345dcddf4b4c9c6a6947d000d52902c30271cf\""
    },
    "AssetParameters974996a9096d42156ceb01e12ea154d428b9b643131593d6d5dbc4dc9d11918fS3Bucket69F99350": {
      "Type": "String",
      "Description": "S3 bucket for asset \"974996a9096d42156ceb01e12ea154d428b9b643131593d6d5dbc4dc9d11918f\""
    },
    "AssetParameters974996a9096d42156ceb01e12ea154d428b9b643131593d6d5dbc4dc9d11918fS3VersionKey160115D9": {
      "Type": "String",
      "Description": "S3 key for asset version \"974996a9096d42156ceb01e12ea154d428b9b643131593d6d5dbc4dc9d11918f\""
    },
    "AssetParameters974996a9096d42156ceb01e12ea154d428b9b643131593d6d5dbc4dc9d11918fArtifactHash41F53E92": {
      "Type": "String",
      "Description": "Artifact hash for asset \"974996a9096d42156ceb01e12ea154d428b9b643131593d6d5dbc4dc9d11918f\""
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