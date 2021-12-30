from tests.utilities import TestTemplates, true, false

class TestCloudWatchDashboard(TestTemplates):

    def test_cloudwatch_dashboard(self):
        self.assert_template_equal(
            'CloudWatchDashboard',
            {
  "Resources": {
    "HttpAPI8D545486": {
      "Type": "AWS::ApiGatewayV2::Api",
      "Properties": {
        "Name": "HttpAPI",
        "ProtocolType": "HTTP"
      },
      "Metadata": {
        "aws:cdk:path": "CloudWatchDashboard/HttpAPI/Resource"
      }
    },
    "HttpAPIDefaultRouteLambdaIntegrationPermission08126EC0": {
      "Type": "AWS::Lambda::Permission",
      "Properties": {
        "Action": "lambda:InvokeFunction",
        "FunctionName": {
          "Fn::ImportValue": "LambdaFunction:ExportsOutputFnGetAttLambdaFunctionBF21E41FArn8BD9CD14"
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
                "Ref": "HttpAPI8D545486"
              },
              "/*/*"
            ]
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "CloudWatchDashboard/HttpAPI/DefaultRoute/LambdaIntegration-Permission"
      }
    },
    "HttpAPIDefaultRouteLambdaIntegration72370CBA": {
      "Type": "AWS::ApiGatewayV2::Integration",
      "Properties": {
        "ApiId": {
          "Ref": "HttpAPI8D545486"
        },
        "IntegrationType": "AWS_PROXY",
        "IntegrationUri": {
          "Fn::ImportValue": "LambdaFunction:ExportsOutputFnGetAttLambdaFunctionBF21E41FArn8BD9CD14"
        },
        "PayloadFormatVersion": "2.0"
      },
      "Metadata": {
        "aws:cdk:path": "CloudWatchDashboard/HttpAPI/DefaultRoute/LambdaIntegration/Resource"
      }
    },
    "HttpAPIDefaultRouteF9949FE6": {
      "Type": "AWS::ApiGatewayV2::Route",
      "Properties": {
        "ApiId": {
          "Ref": "HttpAPI8D545486"
        },
        "RouteKey": "$default",
        "AuthorizationType": "NONE",
        "Target": {
          "Fn::Join": [
            "",
            [
              "integrations/",
              {
                "Ref": "HttpAPIDefaultRouteLambdaIntegration72370CBA"
              }
            ]
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "CloudWatchDashboard/HttpAPI/DefaultRoute/Resource"
      }
    },
    "HttpAPIDefaultStage1BC7D78F": {
      "Type": "AWS::ApiGatewayV2::Stage",
      "Properties": {
        "ApiId": {
          "Ref": "HttpAPI8D545486"
        },
        "StageName": "$default",
        "AutoDeploy": true
      },
      "Metadata": {
        "aws:cdk:path": "CloudWatchDashboard/HttpAPI/DefaultStage/Resource"
      }
    },
    "theBigFanTopicF96567DE": {
      "Type": "AWS::SNS::Topic",
      "Metadata": {
        "aws:cdk:path": "CloudWatchDashboard/theBigFanTopic/Resource"
      }
    },
    "APIGateway4XXErrors1647FE3DB": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "theBigFanTopicF96567DE"
          }
        ],
        "DatapointsToAlarm": 1,
        "Metrics": [
          {
            "Expression": "m1/m2*100",
            "Id": "expr_1",
            "Label": "% API Gateway 4xx Errors"
          },
          {
            "Id": "m1",
            "Label": "4XX Errors",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "ApiId",
                    "Value": {
                      "Ref": "HttpAPI8D545486"
                    }
                  }
                ],
                "MetricName": "4XXError",
                "Namespace": "AWS/ApiGateway"
              },
              "Period": 300,
              "Stat": "Sum",
              "Unit": "Count"
            },
            "ReturnData": false
          },
          {
            "Id": "m2",
            "Label": "# Requests",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "ApiId",
                    "Value": {
                      "Ref": "HttpAPI8D545486"
                    }
                  }
                ],
                "MetricName": "Count",
                "Namespace": "AWS/ApiGateway"
              },
              "Period": 300,
              "Stat": "Sum",
              "Unit": "Count"
            },
            "ReturnData": false
          }
        ],
        "Threshold": 1,
        "TreatMissingData": "notBreaching"
      },
      "Metadata": {
        "aws:cdk:path": "CloudWatchDashboard/API Gateway 4XX Errors > 1%/Resource"
      }
    },
    "APIGateway5XXErrors0A91D7B4E": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "theBigFanTopicF96567DE"
          }
        ],
        "DatapointsToAlarm": 1,
        "Metrics": [
          {
            "Id": "m1",
            "Label": "5XX Errors",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "ApiId",
                    "Value": {
                      "Ref": "HttpAPI8D545486"
                    }
                  }
                ],
                "MetricName": "5XXError",
                "Namespace": "AWS/ApiGateway"
              },
              "Period": 900,
              "Stat": "p99",
              "Unit": "Count"
            },
            "ReturnData": true
          }
        ],
        "Period": 300,
        "Threshold": 0,
        "TreatMissingData": "notBreaching"
      },
      "Metadata": {
        "aws:cdk:path": "CloudWatchDashboard/API Gateway 5XX Errors > 0/Resource"
      }
    },
    "APIp99latencyalarm1s67095ACE": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "theBigFanTopicF96567DE"
          }
        ],
        "DatapointsToAlarm": 1,
        "Metrics": [
          {
            "Id": "m1",
            "Label": "API GW Latency",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "ApiId",
                    "Value": {
                      "Ref": "HttpAPI8D545486"
                    }
                  }
                ],
                "MetricName": "Latency",
                "Namespace": "AWS/ApiGateway"
              },
              "Period": 900,
              "Stat": "p99",
              "Unit": "Count"
            },
            "ReturnData": true
          }
        ],
        "Period": 300,
        "Threshold": 1000,
        "TreatMissingData": "notBreaching"
      },
      "Metadata": {
        "aws:cdk:path": "CloudWatchDashboard/API p99 latency alarm >= 1s/Resource"
      }
    },
    "DynamoLambda2ErrorDE3BEB2F": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "theBigFanTopicF96567DE"
          }
        ],
        "DatapointsToAlarm": 1,
        "Metrics": [
          {
            "Expression": "e / i * 100",
            "Id": "expr_1",
            "Label": "% of invocations that errored, last 5 mins"
          },
          {
            "Id": "i",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "FunctionName",
                    "Value": {
                      "Fn::ImportValue": "LambdaFunction:ExportsOutputRefLambdaFunctionBF21E41F66817B40"
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
                      "Fn::ImportValue": "LambdaFunction:ExportsOutputRefLambdaFunctionBF21E41F66817B40"
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
        "aws:cdk:path": "CloudWatchDashboard/Dynamo Lambda 2% Error/Resource"
      }
    },
    "DynamoLambdap99LongDuration1s739ED568": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "theBigFanTopicF96567DE"
          }
        ],
        "DatapointsToAlarm": 1,
        "Dimensions": [
          {
            "Name": "FunctionName",
            "Value": {
              "Fn::ImportValue": "LambdaFunction:ExportsOutputRefLambdaFunctionBF21E41F66817B40"
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
        "aws:cdk:path": "CloudWatchDashboard/Dynamo Lambda p99 Long Duration (>1s)/Resource"
      }
    },
    "DynamoLambda2Throttled090CFA4C": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "theBigFanTopicF96567DE"
          }
        ],
        "DatapointsToAlarm": 1,
        "Metrics": [
          {
            "Expression": "t / (i + t) * 100",
            "Id": "expr_1",
            "Label": "% of throttled requests, last 30 mins"
          },
          {
            "Id": "i",
            "MetricStat": {
              "Metric": {
                "Dimensions": [
                  {
                    "Name": "FunctionName",
                    "Value": {
                      "Fn::ImportValue": "LambdaFunction:ExportsOutputRefLambdaFunctionBF21E41F66817B40"
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
                      "Fn::ImportValue": "LambdaFunction:ExportsOutputRefLambdaFunctionBF21E41F66817B40"
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
        "aws:cdk:path": "CloudWatchDashboard/Dynamo Lambda 2% Throttled/Resource"
      }
    },
    "DynamoDBTableReadsWritesThrottled13F6F2AE": {
      "Type": "AWS::CloudWatch::Alarm",
      "Properties": {
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "EvaluationPeriods": 6,
        "AlarmActions": [
          {
            "Ref": "theBigFanTopicF96567DE"
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
                      "Fn::ImportValue": "DynamoDBTable:ExportsOutputRefHitsFF5AF8CDC54C3C7B"
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
                      "Fn::ImportValue": "DynamoDBTable:ExportsOutputRefHitsFF5AF8CDC54C3C7B"
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
        "aws:cdk:path": "CloudWatchDashboard/DynamoDB Table Reads--Writes Throttled/Resource"
      }
    },
    "CloudWatchDashBoard043C60B6": {
      "Type": "AWS::CloudWatch::Dashboard",
      "Properties": {
        "DashboardBody": {
          "Fn::Join": [
            "",
            [
              "{\"widgets\":[{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":0,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Requests\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"metrics\":[[\"AWS/ApiGateway\",\"Count\",\"ApiId\",\"",
              {
                "Ref": "HttpAPI8D545486"
              },
              "\",{\"label\":\"# Requests\",\"period\":900,\"stat\":\"Sum\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":8,\"y\":0,\"properties\":{\"view\":\"timeSeries\",\"title\":\"API GW Latency\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":true,\"metrics\":[[\"AWS/ApiGateway\",\"Latency\",\"ApiId\",\"",
              {
                "Ref": "HttpAPI8D545486"
              },
              "\",{\"label\":\"API Latency p50\",\"period\":900,\"stat\":\"p50\"}],[\"AWS/ApiGateway\",\"Latency\",\"ApiId\",\"",
              {
                "Ref": "HttpAPI8D545486"
              },
              "\",{\"label\":\"API Latency p90\",\"period\":900,\"stat\":\"p90\"}],[\"AWS/ApiGateway\",\"Latency\",\"ApiId\",\"",
              {
                "Ref": "HttpAPI8D545486"
              },
              "\",{\"label\":\"API Latency p99\",\"period\":900,\"stat\":\"p99\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":16,\"y\":0,\"properties\":{\"view\":\"timeSeries\",\"title\":\"API GW Errors\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":true,\"metrics\":[[\"AWS/ApiGateway\",\"4XXError\",\"ApiId\",\"",
              {
                "Ref": "HttpAPI8D545486"
              },
              "\",{\"label\":\"4XX Errors\",\"period\":900,\"stat\":\"Sum\"}],[\"AWS/ApiGateway\",\"5XXError\",\"ApiId\",\"",
              {
                "Ref": "HttpAPI8D545486"
              },
              "\",{\"label\":\"5XX Errors\",\"period\":900,\"stat\":\"Sum\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":6,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Dynamo Lambda Error %\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"metrics\":[[{\"label\":\"% of invocations that errored, last 5 mins\",\"expression\":\"e / i * 100\"}],[\"AWS/Lambda\",\"Invocations\",\"FunctionName\",\"",
              {
                "Fn::ImportValue": "LambdaFunction:ExportsOutputRefLambdaFunctionBF21E41F66817B40"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"i\"}],[\"AWS/Lambda\",\"Errors\",\"FunctionName\",\"",
              {
                "Fn::ImportValue": "LambdaFunction:ExportsOutputRefLambdaFunctionBF21E41F66817B40"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"e\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":8,\"y\":6,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Dynamo Lambda Duration\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":true,\"metrics\":[[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Fn::ImportValue": "LambdaFunction:ExportsOutputRefLambdaFunctionBF21E41F66817B40"
              },
              "\",{\"stat\":\"p50\"}],[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Fn::ImportValue": "LambdaFunction:ExportsOutputRefLambdaFunctionBF21E41F66817B40"
              },
              "\",{\"stat\":\"p90\"}],[\"AWS/Lambda\",\"Duration\",\"FunctionName\",\"",
              {
                "Fn::ImportValue": "LambdaFunction:ExportsOutputRefLambdaFunctionBF21E41F66817B40"
              },
              "\",{\"stat\":\"p99\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":16,\"y\":6,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Dynamo Lambda Throttle %\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"metrics\":[[{\"label\":\"% of throttled requests, last 30 mins\",\"expression\":\"t / (i + t) * 100\"}],[\"AWS/Lambda\",\"Invocations\",\"FunctionName\",\"",
              {
                "Fn::ImportValue": "LambdaFunction:ExportsOutputRefLambdaFunctionBF21E41F66817B40"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"i\"}],[\"AWS/Lambda\",\"Throttles\",\"FunctionName\",\"",
              {
                "Fn::ImportValue": "LambdaFunction:ExportsOutputRefLambdaFunctionBF21E41F66817B40"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"t\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":12,\"properties\":{\"view\":\"timeSeries\",\"title\":\"DynamoDB Latency\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":true,\"metrics\":[[\"AWS/DynamoDB\",\"SuccessfulRequestLatency\",\"Operation\",\"GetItem\",\"TableName\",\"",
              {
                "Fn::ImportValue": "DynamoDBTable:ExportsOutputRefHitsFF5AF8CDC54C3C7B"
              },
              "\"],[\"AWS/DynamoDB\",\"SuccessfulRequestLatency\",\"Operation\",\"UpdateItem\",\"TableName\",\"",
              {
                "Fn::ImportValue": "DynamoDBTable:ExportsOutputRefHitsFF5AF8CDC54C3C7B"
              },
              "\"],[\"AWS/DynamoDB\",\"SuccessfulRequestLatency\",\"Operation\",\"PutItem\",\"TableName\",\"",
              {
                "Fn::ImportValue": "DynamoDBTable:ExportsOutputRefHitsFF5AF8CDC54C3C7B"
              },
              "\"],[\"AWS/DynamoDB\",\"SuccessfulRequestLatency\",\"Operation\",\"DeleteItem\",\"TableName\",\"",
              {
                "Fn::ImportValue": "DynamoDBTable:ExportsOutputRefHitsFF5AF8CDC54C3C7B"
              },
              "\"],[\"AWS/DynamoDB\",\"SuccessfulRequestLatency\",\"Operation\",\"Query\",\"TableName\",\"",
              {
                "Fn::ImportValue": "DynamoDBTable:ExportsOutputRefHitsFF5AF8CDC54C3C7B"
              },
              "\"]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":8,\"y\":12,\"properties\":{\"view\":\"timeSeries\",\"title\":\"DynamoDB Consumed Read/Write Units\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":false,\"metrics\":[[\"AWS/DynamoDB\",\"ConsumedReadCapacityUnits\",\"TableName\",\"",
              {
                "Fn::ImportValue": "DynamoDBTable:ExportsOutputRefHitsFF5AF8CDC54C3C7B"
              },
              "\"],[\"AWS/DynamoDB\",\"ConsumedWriteCapacityUnits\",\"TableName\",\"",
              {
                "Fn::ImportValue": "DynamoDBTable:ExportsOutputRefHitsFF5AF8CDC54C3C7B"
              },
              "\"]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":16,\"y\":12,\"properties\":{\"view\":\"timeSeries\",\"title\":\"DynamoDB Throttles\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":true,\"metrics\":[[\"AWS/DynamoDB\",\"ReadThrottleEvents\",\"TableName\",\"",
              {
                "Fn::ImportValue": "DynamoDBTable:ExportsOutputRefHitsFF5AF8CDC54C3C7B"
              },
              "\",{\"stat\":\"Sum\"}],[\"AWS/DynamoDB\",\"WriteThrottleEvents\",\"TableName\",\"",
              {
                "Fn::ImportValue": "DynamoDBTable:ExportsOutputRefHitsFF5AF8CDC54C3C7B"
              },
              "\",{\"stat\":\"Sum\"}]],\"yAxis\":{}}}]}"
            ]
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "CloudWatchDashboard/CloudWatchDashBoard/Resource"
      }
    },
    "CDKMetadata": {
      "Type": "AWS::CDK::Metadata",
      "Properties": {
        "Analytics": "v2:deflate64:H4sIAAAAAAAA/12OTU4DMQyFz9J96nbogi1VWdAV1cAF3CTMmM4kUeIwqqLcnXGQQGLl7z0//3TQHR5hv3nCJW21ue2K9tFCeWPUN3X6cK+ZQ2Z18i5xzJrF623yOWorvDYMMXlXlawoGGhAtgvevx6gvDCHYyAJShHZ+8y20dmxHSLKsAT+yb/c+svQbjWoasL5ahBW42LjTCnJRHIJyrsPpCXZoCo9+WwWZD1COU4Y5/ZIg2dM49VjNGL9ilqrutx59G53gG4P3eYzEW1jdkyzhf6nfgPzVOWrNQEAAA=="
      },
      "Metadata": {
        "aws:cdk:path": "CloudWatchDashboard/CDKMetadata/Default"
      },
      "Condition": "CDKMetadataAvailable"
    }
  },
  "Outputs": {
    "HTTPAPIUrl": {
      "Value": {
        "Fn::Join": [
          "",
          [
            "https://",
            {
              "Ref": "HttpAPI8D545486"
            },
            ".execute-api.",
            {
              "Ref": "AWS::Region"
            },
            ".",
            {
              "Ref": "AWS::URLSuffix"
            },
            "/"
          ]
        ]
      }
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