from tests.utilities import TestTemplates, true, false

class TestHTTPAPICloudWatchDashboard(TestTemplates):

    def test_http_api_cloudwatch_dashboard(self):
        self.assert_template_equal(
            'HttpApiCloudWatchDashboard',
             {
  "Resources": {
    "CloudWatchDashBoard043C60B6": {
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
                "Fn::ImportValue": "LambdaFunction:ExportsOutputRefLambdaFunctionBF21E41F66817B40"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"invocations\"}],[\"AWS/Lambda\",\"Errors\",\"FunctionName\",\"",
              {
                "Fn::ImportValue": "LambdaFunction:ExportsOutputRefLambdaFunctionBF21E41F66817B40"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"e\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":8,\"y\":0,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Dynamo Lambda Duration\",\"region\":\"",
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
              "\",{\"stat\":\"p99\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":16,\"y\":0,\"properties\":{\"view\":\"timeSeries\",\"title\":\"Dynamo Lambda Throttle %\",\"region\":\"",
              {
                "Ref": "AWS::Region"
              },
              "\",\"stacked\":false,\"metrics\":[[{\"label\":\"% of throttled requests, last 30 mins\",\"expression\":\"t / (invocations + t) * 100\"}],[\"AWS/Lambda\",\"Invocations\",\"FunctionName\",\"",
              {
                "Fn::ImportValue": "LambdaFunction:ExportsOutputRefLambdaFunctionBF21E41F66817B40"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"invocations\"}],[\"AWS/Lambda\",\"Throttles\",\"FunctionName\",\"",
              {
                "Fn::ImportValue": "LambdaFunction:ExportsOutputRefLambdaFunctionBF21E41F66817B40"
              },
              "\",{\"stat\":\"Sum\",\"visible\":false,\"id\":\"t\"}]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":0,\"y\":6,\"properties\":{\"view\":\"timeSeries\",\"title\":\"DynamoDB Latency\",\"region\":\"",
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
              "\"]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":8,\"y\":6,\"properties\":{\"view\":\"timeSeries\",\"title\":\"DynamoDB Consumed Read/Write Units\",\"region\":\"",
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
              "\"]],\"yAxis\":{}}},{\"type\":\"metric\",\"width\":8,\"height\":6,\"x\":16,\"y\":6,\"properties\":{\"view\":\"timeSeries\",\"title\":\"DynamoDB Throttles\",\"region\":\"",
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
        "aws:cdk:path": "HttpApiCloudWatchDashboard/CloudWatchDashBoard/Resource"
      }
    },
    "CDKMetadata": {
      "Type": "AWS::CDK::Metadata",
      "Properties": {
        "Analytics": "v2:deflate64:H4sIAAAAAAAA/z2LQQrCMBBFz9J9Om3owq1QDyD1BOMkklidgWRCkZC7axVc/f/471uw0wHG7ohb7smtQyVJHupFkVYzC2dNhdTMN158lpLI7/0zuKhRuJnv8SHFbagUoJ4wh6tgcrv3h9bM+aVBeJjAjmC7e46xT4U1Pj0sv3wDD+rrNo0AAAA="
      },
      "Metadata": {
        "aws:cdk:path": "HttpApiCloudWatchDashboard/CDKMetadata/Default"
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
  }
}
      )