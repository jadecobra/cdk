from tests.utilities import TestTemplates, true, false


class TestHTTPAPI(TestTemplates):

    def test_http_api_gateway(self):
        self.assert_template_equal(
            'LambdaHttpApiGateway',
            {
  "Resources": {
    "HttpAPI8D545486": {
      "Type": "AWS::ApiGatewayV2::Api",
      "Properties": {
        "Name": "HttpAPI",
        "ProtocolType": "HTTP"
      }
    },
    "HttpAPIDefaultRouteHTTPLambdaIntegrationPermission5A5BB64C": {
      "Type": "AWS::Lambda::Permission",
      "Properties": {
        "Action": "lambda:InvokeFunction",
        "FunctionName": {
          "Fn::ImportValue": "LambdaFunction:ExportsOutputFnGetAtthitcounterLambdaFunctionB862C182Arn3B74EE41"
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
      }
    },
    "HttpAPIDefaultRouteHTTPLambdaIntegration7A40D12F": {
      "Type": "AWS::ApiGatewayV2::Integration",
      "Properties": {
        "ApiId": {
          "Ref": "HttpAPI8D545486"
        },
        "IntegrationType": "AWS_PROXY",
        "IntegrationUri": {
          "Fn::ImportValue": "LambdaFunction:ExportsOutputFnGetAtthitcounterLambdaFunctionB862C182Arn3B74EE41"
        },
        "PayloadFormatVersion": "2.0"
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
                "Ref": "HttpAPIDefaultRouteHTTPLambdaIntegration7A40D12F"
              }
            ]
          ]
        }
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
      }
    },
    "ApiGatewayCloudWatchErrorTopicB01304FE": {
      "Type": "AWS::SNS::Topic",
      "Properties": {
        "DisplayName": "ErrorTopic"
      }
    },
    "ApiGatewayCloudWatchAPIGateway4XXErrors11FFC618F": {
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
      }
    },
    "ApiGatewayCloudWatchAPIGateway5XXErrors0001B6606": {
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
        "Threshold": 0,
        "TreatMissingData": "notBreaching"
      }
    },
    "ApiGatewayCloudWatchAPIp99latencyalarm1s6545CFD1": {
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
        "Threshold": 1000,
        "TreatMissingData": "notBreaching"
      }
    },
    "ApiGatewayCloudWatchCloudWatchDashBoard278188F3": {
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
              "\",\"stacked\":false,\"metrics\":[[\"AWS/ApiGateway\",\"Count\",\"ApiId\",\"",
              {
                "Ref": "HttpAPI8D545486"
              },
              "\",{\"label\":\"# Requests\",\"period\":900,\"stat\":\"Sum\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":6,\"properties\":{\"view\":\"timeSeries\",\"title\":\"API GW Latency\",\"region\":\"",
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
              "\",{\"label\":\"API Latency p99\",\"period\":900,\"stat\":\"p99\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":12,\"properties\":{\"view\":\"timeSeries\",\"title\":\"API GW Errors\",\"region\":\"",
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
              "\",{\"label\":\"5XX Errors\",\"period\":900,\"stat\":\"Sum\"}]],\"yAxis\":{}}}]}"
            ]
          ]
        }
      }
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
  }
}
        )