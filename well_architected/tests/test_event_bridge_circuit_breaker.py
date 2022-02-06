from tests.utilities import TestTemplates, true, false

class TestEventBridgeCircuitBreaker(TestTemplates):

    def test_event_bridge_circuit_breaker(self):
        self.assert_template_equal(
            'EventBridgeCircuitBreaker',
            {
  "Resources": {
    "CircuitBreaker4FAEA3DB": {
      "Type": "AWS::DynamoDB::Table",
      "Properties": {
        "KeySchema": [
          {
            "AttributeName": "RequestID",
            "KeyType": "HASH"
          },
          {
            "AttributeName": "ExpirationTime",
            "KeyType": "RANGE"
          }
        ],
        "AttributeDefinitions": [
          {
            "AttributeName": "RequestID",
            "AttributeType": "S"
          },
          {
            "AttributeName": "ExpirationTime",
            "AttributeType": "N"
          },
          {
            "AttributeName": "SiteUrl",
            "AttributeType": "S"
          }
        ],
        "GlobalSecondaryIndexes": [
          {
            "IndexName": "UrlIndex",
            "KeySchema": [
              {
                "AttributeName": "SiteUrl",
                "KeyType": "HASH"
              },
              {
                "AttributeName": "ExpirationTime",
                "KeyType": "RANGE"
              }
            ],
            "Projection": {
              "ProjectionType": "ALL"
            },
            "ProvisionedThroughput": {
              "ReadCapacityUnits": 5,
              "WriteCapacityUnits": 5
            }
          }
        ],
        "ProvisionedThroughput": {
          "ReadCapacityUnits": 5,
          "WriteCapacityUnits": 5
        },
        "TimeToLiveSpecification": {
          "AttributeName": "ExpirationTime",
          "Enabled": true
        }
      },
      "UpdateReplacePolicy": "Retain",
      "DeletionPolicy": "Retain"
    },
    "webserviceErrorTopic186C4EDE": {
      "Type": "AWS::SNS::Topic",
      "Properties": {
        "DisplayName": "ErrorTopic"
      }
    },
    "webserviceawsxraysdkLambdaLayer9B4551BE": {
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
      }
    },
    "webserviceLambdaFunctionServiceRole834310C5": {
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
      }
    },
    "webserviceLambdaFunctionServiceRoleDefaultPolicyE1BC4E3D": {
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
                "dynamodb:ConditionCheckItem"
              ],
              "Effect": "Allow",
              "Resource": [
                {
                  "Fn::GetAtt": [
                    "CircuitBreaker4FAEA3DB",
                    "Arn"
                  ]
                },
                {
                  "Fn::Join": [
                    "",
                    [
                      {
                        "Fn::GetAtt": [
                          "CircuitBreaker4FAEA3DB",
                          "Arn"
                        ]
                      },
                      "/index/*"
                    ]
                  ]
                }
              ]
            },
            {
              "Action": "events:PutEvents",
              "Effect": "Allow",
              "Resource": "*"
            }
          ],
          "Version": "2012-10-17"
        },
        "PolicyName": "webserviceLambdaFunctionServiceRoleDefaultPolicyE1BC4E3D",
        "Roles": [
          {
            "Ref": "webserviceLambdaFunctionServiceRole834310C5"
          }
        ]
      }
    },
    "webserviceLambdaFunctionB896CD05": {
      "Type": "AWS::Lambda::Function",
      "Properties": {
        "Code": {
          "S3Bucket": {
            "Ref": "AssetParametersd8fa8924b42700edfd14edbb97f11c331ada47e843cf4468b9b8645047e1a005S3Bucket22582398"
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
                          "Ref": "AssetParametersd8fa8924b42700edfd14edbb97f11c331ada47e843cf4468b9b8645047e1a005S3VersionKey9DB7E1DD"
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
                          "Ref": "AssetParametersd8fa8924b42700edfd14edbb97f11c331ada47e843cf4468b9b8645047e1a005S3VersionKey9DB7E1DD"
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
            "webserviceLambdaFunctionServiceRole834310C5",
            "Arn"
          ]
        },
        "Environment": {
          "Variables": {
            "TABLE_NAME": {
              "Ref": "CircuitBreaker4FAEA3DB"
            }
          }
        },
        "Handler": "webservice.handler",
        "Layers": [
          {
            "Ref": "webserviceawsxraysdkLambdaLayer9B4551BE"
          }
        ],
        "Runtime": "python3.8",
        "Timeout": 20,
        "TracingConfig": {
          "Mode": "Active"
        }
      },
      "DependsOn": [
        "webserviceLambdaFunctionServiceRoleDefaultPolicyE1BC4E3D",
        "webserviceLambdaFunctionServiceRole834310C5"
      ]
    },
    "webserviceLambdainvocationErrors285D2B84E": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "webserviceErrorTopic186C4EDE"
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
                      "Ref": "webserviceLambdaFunctionB896CD05"
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
                      "Ref": "webserviceLambdaFunctionB896CD05"
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
      }
    },
    "webserviceLambdap99LongDuration1s702ADBFE": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "webserviceErrorTopic186C4EDE"
          }
        ],
        "DatapointsToAlarm": 1,
        "Dimensions": [
          {
            "Name": "FunctionName",
            "Value": {
              "Ref": "webserviceLambdaFunctionB896CD05"
            }
          }
        ],
        "ExtendedStatistic": "p99",
        "MetricName": "Duration",
        "Namespace": "AWS/Lambda",
        "Period": 300,
        "Threshold": 1000,
        "TreatMissingData": "notBreaching"
      }
    },
    "webserviceLambdaThrottledinvocations29B11B89F": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "webserviceErrorTopic186C4EDE"
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
                      "Ref": "webserviceLambdaFunctionB896CD05"
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
                      "Ref": "webserviceLambdaFunctionB896CD05"
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
      }
    },
    "webserviceCloudWatchDashBoard47AAFEDA": {
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
                "Ref": "webserviceLambdaFunctionB896CD05"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"invocations\"}],[\"AWS/Lambda\",\"Errors\",\"FunctionName\",\"",
              {
                "Ref": "webserviceLambdaFunctionB896CD05"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"errors\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":6,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Lambda Duration\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":true,\"metrics\":[[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "webserviceLambdaFunctionB896CD05"
              },
              "\",{\"stat\":\"p50\"}],[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "webserviceLambdaFunctionB896CD05"
              },
              "\",{\"stat\":\"p90\"}],[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "webserviceLambdaFunctionB896CD05"
              },
              "\",{\"stat\":\"p99\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":12,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Lambda Throttle %\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":false,\"metrics\":[[{\"label\":\"throttled requests % in last 30 mins\",\"expression\":\"(throttles * 100) / (invocations + throttles)\"}],[\"AWS/Lambda\",\"Invocations\",\"FunctionName\",\"",
              {
                "Ref": "webserviceLambdaFunctionB896CD05"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"invocations\"}],[\"AWS/Lambda\",\"Throttles\",\"FunctionName\",\"",
              {
                "Ref": "webserviceLambdaFunctionB896CD05"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"throttles\"}]],\"yAxis\":{}}}]}"
            ]
          ]
        }
      }
    },
    "errorErrorTopicE7B6AD64": {
      "Type": "AWS::SNS::Topic",
      "Properties": {
        "DisplayName": "ErrorTopic"
      }
    },
    "errorawsxraysdkLambdaLayer7963DA8A": {
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
      }
    },
    "errorLambdaFunctionServiceRoleBA0401A4": {
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
      }
    },
    "errorLambdaFunctionServiceRoleDefaultPolicy7F656B38": {
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
                "dynamodb:BatchWriteItem",
                "dynamodb:PutItem",
                "dynamodb:UpdateItem",
                "dynamodb:DeleteItem"
              ],
              "Effect": "Allow",
              "Resource": [
                {
                  "Fn::GetAtt": [
                    "CircuitBreaker4FAEA3DB",
                    "Arn"
                  ]
                },
                {
                  "Fn::Join": [
                    "",
                    [
                      {
                        "Fn::GetAtt": [
                          "CircuitBreaker4FAEA3DB",
                          "Arn"
                        ]
                      },
                      "/index/*"
                    ]
                  ]
                }
              ]
            }
          ],
          "Version": "2012-10-17"
        },
        "PolicyName": "errorLambdaFunctionServiceRoleDefaultPolicy7F656B38",
        "Roles": [
          {
            "Ref": "errorLambdaFunctionServiceRoleBA0401A4"
          }
        ]
      }
    },
    "errorLambdaFunction47F9F7B6": {
      "Type": "AWS::Lambda::Function",
      "Properties": {
        "Code": {
          "S3Bucket": {
            "Ref": "AssetParameters762c39aa63007144d6cb020489a92b28917b4e5d27564e6bff7f7d6c3fd5200bS3Bucket93AD9C3D"
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
                          "Ref": "AssetParameters762c39aa63007144d6cb020489a92b28917b4e5d27564e6bff7f7d6c3fd5200bS3VersionKey61994CBC"
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
                          "Ref": "AssetParameters762c39aa63007144d6cb020489a92b28917b4e5d27564e6bff7f7d6c3fd5200bS3VersionKey61994CBC"
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
            "errorLambdaFunctionServiceRoleBA0401A4",
            "Arn"
          ]
        },
        "Environment": {
          "Variables": {
            "TABLE_NAME": {
              "Ref": "CircuitBreaker4FAEA3DB"
            }
          }
        },
        "Handler": "error.handler",
        "Layers": [
          {
            "Ref": "errorawsxraysdkLambdaLayer7963DA8A"
          }
        ],
        "Runtime": "python3.8",
        "Timeout": 3,
        "TracingConfig": {
          "Mode": "Active"
        }
      },
      "DependsOn": [
        "errorLambdaFunctionServiceRoleDefaultPolicy7F656B38",
        "errorLambdaFunctionServiceRoleBA0401A4"
      ]
    },
    "errorLambdainvocationErrors24E6C9E5A": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "errorErrorTopicE7B6AD64"
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
                      "Ref": "errorLambdaFunction47F9F7B6"
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
                      "Ref": "errorLambdaFunction47F9F7B6"
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
      }
    },
    "errorLambdap99LongDuration1sBDA60A03": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "errorErrorTopicE7B6AD64"
          }
        ],
        "DatapointsToAlarm": 1,
        "Dimensions": [
          {
            "Name": "FunctionName",
            "Value": {
              "Ref": "errorLambdaFunction47F9F7B6"
            }
          }
        ],
        "ExtendedStatistic": "p99",
        "MetricName": "Duration",
        "Namespace": "AWS/Lambda",
        "Period": 300,
        "Threshold": 1000,
        "TreatMissingData": "notBreaching"
      }
    },
    "errorLambdaThrottledinvocations286DE33FD": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "errorErrorTopicE7B6AD64"
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
                      "Ref": "errorLambdaFunction47F9F7B6"
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
                      "Ref": "errorLambdaFunction47F9F7B6"
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
      }
    },
    "errorCloudWatchDashBoardDDFEAB71": {
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
                "Ref": "errorLambdaFunction47F9F7B6"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"invocations\"}],[\"AWS/Lambda\",\"Errors\",\"FunctionName\",\"",
              {
                "Ref": "errorLambdaFunction47F9F7B6"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"errors\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":6,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Lambda Duration\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":true,\"metrics\":[[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "errorLambdaFunction47F9F7B6"
              },
              "\",{\"stat\":\"p50\"}],[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "errorLambdaFunction47F9F7B6"
              },
              "\",{\"stat\":\"p90\"}],[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Ref": "errorLambdaFunction47F9F7B6"
              },
              "\",{\"stat\":\"p99\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":12,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Lambda Throttle %\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":false,\"metrics\":[[{\"label\":\"throttled requests % in last 30 mins\",\"expression\":\"(throttles * 100) / (invocations + throttles)\"}],[\"AWS/Lambda\",\"Invocations\",\"FunctionName\",\"",
              {
                "Ref": "errorLambdaFunction47F9F7B6"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"invocations\"}],[\"AWS/Lambda\",\"Throttles\",\"FunctionName\",\"",
              {
                "Ref": "errorLambdaFunction47F9F7B6"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"throttles\"}]],\"yAxis\":{}}}]}"
            ]
          ]
        }
      }
    },
    "webserviceErrorRuleCE293636": {
      "Type": "AWS::Events::Rule",
      "Properties": {
        "Description": "Failed Webservice Call",
        "EventPattern": {
          "detail": {
            "status": [
              "fail"
            ]
          },
          "detail-type": [
            "httpcall"
          ],
          "source": [
            "cdkpatterns.eventbridge.circuitbreaker"
          ]
        },
        "State": "ENABLED",
        "Targets": [
          {
            "Arn": {
              "Fn::GetAtt": [
                "errorLambdaFunction47F9F7B6",
                "Arn"
              ]
            },
            "Id": "Target0"
          }
        ]
      }
    },
    "webserviceErrorRuleAllowEventRuleEventBridgeCircuitBreakererrorLambdaFunction3A1EB0D3E1DFE36A": {
      "Type": "AWS::Lambda::Permission",
      "Properties": {
        "Action": "lambda:InvokeFunction",
        "FunctionName": {
          "Fn::GetAtt": [
            "errorLambdaFunction47F9F7B6",
            "Arn"
          ]
        },
        "Principal": "events.amazonaws.com",
        "SourceArn": {
          "Fn::GetAtt": [
            "webserviceErrorRuleCE293636",
            "Arn"
          ]
        }
      }
    },
    "CircuitBreakerGateway122B123C": {
      "Type": "AWS::ApiGateway::RestApi",
      "Properties": {
        "Name": "CircuitBreakerGateway"
      }
    },
    "CircuitBreakerGatewayCloudWatchRole934DF897": {
      "Type": "AWS::IAM::Role",
      "Properties": {
        "AssumeRolePolicyDocument": {
          "Statement": [
            {
              "Action": "sts:AssumeRole",
              "Effect": "Allow",
              "Principal": {
                "Service": "apigateway.amazonaws.com"
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
                ":iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs"
              ]
            ]
          }
        ]
      }
    },
    "CircuitBreakerGatewayAccount58B91765": {
      "Type": "AWS::ApiGateway::Account",
      "Properties": {
        "CloudWatchRoleArn": {
          "Fn::GetAtt": [
            "CircuitBreakerGatewayCloudWatchRole934DF897",
            "Arn"
          ]
        }
      },
      "DependsOn": [
        "CircuitBreakerGateway122B123C"
      ]
    },
    "CircuitBreakerGatewayDeployment9F2A82FA1735fcaff60de46340a0d2a3525fb797": {
      "Type": "AWS::ApiGateway::Deployment",
      "Properties": {
        "RestApiId": {
          "Ref": "CircuitBreakerGateway122B123C"
        },
        "Description": "Automatically created by the RestApi construct"
      },
      "DependsOn": [
        "CircuitBreakerGatewayproxyANY759880DB",
        "CircuitBreakerGatewayproxy1147E2CF",
        "CircuitBreakerGatewayANYE076316B"
      ]
    },
    "CircuitBreakerGatewayDeploymentStageprod84F6B9E5": {
      "Type": "AWS::ApiGateway::Stage",
      "Properties": {
        "RestApiId": {
          "Ref": "CircuitBreakerGateway122B123C"
        },
        "DeploymentId": {
          "Ref": "CircuitBreakerGatewayDeployment9F2A82FA1735fcaff60de46340a0d2a3525fb797"
        },
        "StageName": "prod"
      },
      "DependsOn": [
        "CircuitBreakerGatewayAccount58B91765"
      ]
    },
    "CircuitBreakerGatewayproxy1147E2CF": {
      "Type": "AWS::ApiGateway::Resource",
      "Properties": {
        "ParentId": {
          "Fn::GetAtt": [
            "CircuitBreakerGateway122B123C",
            "RootResourceId"
          ]
        },
        "PathPart": "{proxy+}",
        "RestApiId": {
          "Ref": "CircuitBreakerGateway122B123C"
        }
      }
    },
    "CircuitBreakerGatewayproxyANYApiPermissionEventBridgeCircuitBreakerCircuitBreakerGatewayE76DF368ANYproxyD50E72F3": {
      "Type": "AWS::Lambda::Permission",
      "Properties": {
        "Action": "lambda:InvokeFunction",
        "FunctionName": {
          "Fn::GetAtt": [
            "webserviceLambdaFunctionB896CD05",
            "Arn"
          ]
        },
        "Principal": "apigateway.amazonaws.com",
        "SourceArn": {
          "Fn::Join": [
            "",
            [
              "arn:",
              {
                "Ref": "AWS::Partition"
              },
              ":execute-api:",
              {
                "Ref": "AWS::Region"
              },
              ":",
              {
                "Ref": "AWS::AccountId"
              },
              ":",
              {
                "Ref": "CircuitBreakerGateway122B123C"
              },
              "/",
              {
                "Ref": "CircuitBreakerGatewayDeploymentStageprod84F6B9E5"
              },
              "/*/*"
            ]
          ]
        }
      }
    },
    "CircuitBreakerGatewayproxyANYApiPermissionTestEventBridgeCircuitBreakerCircuitBreakerGatewayE76DF368ANYproxyC0DC0845": {
      "Type": "AWS::Lambda::Permission",
      "Properties": {
        "Action": "lambda:InvokeFunction",
        "FunctionName": {
          "Fn::GetAtt": [
            "webserviceLambdaFunctionB896CD05",
            "Arn"
          ]
        },
        "Principal": "apigateway.amazonaws.com",
        "SourceArn": {
          "Fn::Join": [
            "",
            [
              "arn:",
              {
                "Ref": "AWS::Partition"
              },
              ":execute-api:",
              {
                "Ref": "AWS::Region"
              },
              ":",
              {
                "Ref": "AWS::AccountId"
              },
              ":",
              {
                "Ref": "CircuitBreakerGateway122B123C"
              },
              "/test-invoke-stage/*/*"
            ]
          ]
        }
      }
    },
    "CircuitBreakerGatewayproxyANY759880DB": {
      "Type": "AWS::ApiGateway::Method",
      "Properties": {
        "HttpMethod": "ANY",
        "ResourceId": {
          "Ref": "CircuitBreakerGatewayproxy1147E2CF"
        },
        "RestApiId": {
          "Ref": "CircuitBreakerGateway122B123C"
        },
        "AuthorizationType": "NONE",
        "Integration": {
          "IntegrationHttpMethod": "POST",
          "Type": "AWS_PROXY",
          "Uri": {
            "Fn::Join": [
              "",
              [
                "arn:",
                {
                  "Ref": "AWS::Partition"
                },
                ":apigateway:",
                {
                  "Ref": "AWS::Region"
                },
                ":lambda:path/2015-03-31/functions/",
                {
                  "Fn::GetAtt": [
                    "webserviceLambdaFunctionB896CD05",
                    "Arn"
                  ]
                },
                "/invocations"
              ]
            ]
          }
        }
      }
    },
    "CircuitBreakerGatewayANYApiPermissionEventBridgeCircuitBreakerCircuitBreakerGatewayE76DF368ANYFA6718D8": {
      "Type": "AWS::Lambda::Permission",
      "Properties": {
        "Action": "lambda:InvokeFunction",
        "FunctionName": {
          "Fn::GetAtt": [
            "webserviceLambdaFunctionB896CD05",
            "Arn"
          ]
        },
        "Principal": "apigateway.amazonaws.com",
        "SourceArn": {
          "Fn::Join": [
            "",
            [
              "arn:",
              {
                "Ref": "AWS::Partition"
              },
              ":execute-api:",
              {
                "Ref": "AWS::Region"
              },
              ":",
              {
                "Ref": "AWS::AccountId"
              },
              ":",
              {
                "Ref": "CircuitBreakerGateway122B123C"
              },
              "/",
              {
                "Ref": "CircuitBreakerGatewayDeploymentStageprod84F6B9E5"
              },
              "/*/"
            ]
          ]
        }
      }
    },
    "CircuitBreakerGatewayANYApiPermissionTestEventBridgeCircuitBreakerCircuitBreakerGatewayE76DF368ANYB37962A7": {
      "Type": "AWS::Lambda::Permission",
      "Properties": {
        "Action": "lambda:InvokeFunction",
        "FunctionName": {
          "Fn::GetAtt": [
            "webserviceLambdaFunctionB896CD05",
            "Arn"
          ]
        },
        "Principal": "apigateway.amazonaws.com",
        "SourceArn": {
          "Fn::Join": [
            "",
            [
              "arn:",
              {
                "Ref": "AWS::Partition"
              },
              ":execute-api:",
              {
                "Ref": "AWS::Region"
              },
              ":",
              {
                "Ref": "AWS::AccountId"
              },
              ":",
              {
                "Ref": "CircuitBreakerGateway122B123C"
              },
              "/test-invoke-stage/*/"
            ]
          ]
        }
      }
    },
    "CircuitBreakerGatewayANYE076316B": {
      "Type": "AWS::ApiGateway::Method",
      "Properties": {
        "HttpMethod": "ANY",
        "ResourceId": {
          "Fn::GetAtt": [
            "CircuitBreakerGateway122B123C",
            "RootResourceId"
          ]
        },
        "RestApiId": {
          "Ref": "CircuitBreakerGateway122B123C"
        },
        "AuthorizationType": "NONE",
        "Integration": {
          "IntegrationHttpMethod": "POST",
          "Type": "AWS_PROXY",
          "Uri": {
            "Fn::Join": [
              "",
              [
                "arn:",
                {
                  "Ref": "AWS::Partition"
                },
                ":apigateway:",
                {
                  "Ref": "AWS::Region"
                },
                ":lambda:path/2015-03-31/functions/",
                {
                  "Fn::GetAtt": [
                    "webserviceLambdaFunctionB896CD05",
                    "Arn"
                  ]
                },
                "/invocations"
              ]
            ]
          }
        }
      }
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
    "AssetParametersd8fa8924b42700edfd14edbb97f11c331ada47e843cf4468b9b8645047e1a005S3Bucket22582398": {
      "Type": "String",
      "Description": "S3 bucket for asset \"d8fa8924b42700edfd14edbb97f11c331ada47e843cf4468b9b8645047e1a005\""
    },
    "AssetParametersd8fa8924b42700edfd14edbb97f11c331ada47e843cf4468b9b8645047e1a005S3VersionKey9DB7E1DD": {
      "Type": "String",
      "Description": "S3 key for asset version \"d8fa8924b42700edfd14edbb97f11c331ada47e843cf4468b9b8645047e1a005\""
    },
    "AssetParametersd8fa8924b42700edfd14edbb97f11c331ada47e843cf4468b9b8645047e1a005ArtifactHash9CDFA287": {
      "Type": "String",
      "Description": "Artifact hash for asset \"d8fa8924b42700edfd14edbb97f11c331ada47e843cf4468b9b8645047e1a005\""
    },
    "AssetParameters762c39aa63007144d6cb020489a92b28917b4e5d27564e6bff7f7d6c3fd5200bS3Bucket93AD9C3D": {
      "Type": "String",
      "Description": "S3 bucket for asset \"762c39aa63007144d6cb020489a92b28917b4e5d27564e6bff7f7d6c3fd5200b\""
    },
    "AssetParameters762c39aa63007144d6cb020489a92b28917b4e5d27564e6bff7f7d6c3fd5200bS3VersionKey61994CBC": {
      "Type": "String",
      "Description": "S3 key for asset version \"762c39aa63007144d6cb020489a92b28917b4e5d27564e6bff7f7d6c3fd5200b\""
    },
    "AssetParameters762c39aa63007144d6cb020489a92b28917b4e5d27564e6bff7f7d6c3fd5200bArtifactHash305C4958": {
      "Type": "String",
      "Description": "Artifact hash for asset \"762c39aa63007144d6cb020489a92b28917b4e5d27564e6bff7f7d6c3fd5200b\""
    }
  },
  "Outputs": {
    "CircuitBreakerGatewayEndpoint85026A5E": {
      "Value": {
        "Fn::Join": [
          "",
          [
            "https://",
            {
              "Ref": "CircuitBreakerGateway122B123C"
            },
            ".execute-api.",
            {
              "Ref": "AWS::Region"
            },
            ".",
            {
              "Ref": "AWS::URLSuffix"
            },
            "/",
            {
              "Ref": "CircuitBreakerGatewayDeploymentStageprod84F6B9E5"
            },
            "/"
          ]
        ]
      }
    }
  }
}
        )