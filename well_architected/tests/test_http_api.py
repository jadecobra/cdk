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
      },
      "Metadata": {
        "aws:cdk:path": "LambdaHttpApiGateway/HttpAPI/Resource"
      }
    },
    "HttpAPIDefaultRouteHTTPLambdaIntegrationPermission5A5BB64C": {
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
        "aws:cdk:path": "LambdaHttpApiGateway/HttpAPI/DefaultRoute/HTTPLambdaIntegration-Permission"
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
          "Fn::ImportValue": "LambdaFunction:ExportsOutputFnGetAttLambdaFunctionBF21E41FArn8BD9CD14"
        },
        "PayloadFormatVersion": "2.0"
      },
      "Metadata": {
        "aws:cdk:path": "LambdaHttpApiGateway/HttpAPI/DefaultRoute/HTTPLambdaIntegration/Resource"
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
      },
      "Metadata": {
        "aws:cdk:path": "LambdaHttpApiGateway/HttpAPI/DefaultRoute/Resource"
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
        "aws:cdk:path": "LambdaHttpApiGateway/HttpAPI/DefaultStage/Resource"
      }
    },
    "CDKMetadata": {
      "Type": "AWS::CDK::Metadata",
      "Properties": {
        "Analytics": "v2:deflate64:H4sIAAAAAAAA/11OSw6CMBA9C/syUFm41bDRlQRPUEvFirRNO5WQhrvL4MLE1fvMm3nDgVd7KLODmEIuu6FI0noF6YpCDqy+m0tEF5HV1gT0USJ5rQo2eqmIr4NOo7ZmYXQiCad7gWoS83sH6YTojk5TkIBkayOqjZ0Nqt4LWqbAn/zl1l/6rWsjC3uJ8dYJWI1G+VGHQO0La2Z8WFNUwEvg2TNonftoUI8K2i9+AANcqQDtAAAA"
      },
      "Metadata": {
        "aws:cdk:path": "LambdaHttpApiGateway/CDKMetadata/Default"
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
    },
    "ExportsOutputRefHttpAPI8D545486FD78B06F": {
      "Value": {
        "Ref": "HttpAPI8D545486"
      },
      "Export": {
        "Name": "LambdaHttpApiGateway:ExportsOutputRefHttpAPI8D545486FD78B06F"
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