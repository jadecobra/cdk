from tests.utilities import TestTemplates, true, false


class TestHTTPAPI(TestTemplates):

    def test_http_api_gateway(self):
        self.assert_template_equal(
            'LambdaHTTPAPIGateway',
            {
  "Resources": {
    "HttpAPI8D545486": {
      "Type": "AWS::ApiGatewayV2::Api",
      "Properties": {
        "Name": "HttpAPI",
        "ProtocolType": "HTTP"
      },
      "Metadata": {
        "aws:cdk:path": "LambdaHTTPAPIGateway/HttpAPI/Resource"
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
        "aws:cdk:path": "LambdaHTTPAPIGateway/HttpAPI/DefaultRoute/HTTPLambdaIntegration-Permission"
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
        "aws:cdk:path": "LambdaHTTPAPIGateway/HttpAPI/DefaultRoute/HTTPLambdaIntegration/Resource"
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
        "aws:cdk:path": "LambdaHTTPAPIGateway/HttpAPI/DefaultRoute/Resource"
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
        "aws:cdk:path": "LambdaHTTPAPIGateway/HttpAPI/DefaultStage/Resource"
      }
    },
    "CDKMetadata": {
      "Type": "AWS::CDK::Metadata",
      "Properties": {
        "Analytics": "v2:deflate64:H4sIAAAAAAAA/11OQQ6CMBB8C/e6UDl41XDRG8EXrKXiirSk3UpIw9+leDDxNDO7M5mRIMsDFNkRJ79TbZ9HZZ2GeGVUvais8eyCYlHdTaO9DU7pxNdHS0zWLCIFI47UIesJ5/ce4pl5PI2UjAmSbGxgvbGLYd05TOFk+JM/37qg27o2sogXDrcWYT3U2g3kfWpfRD3zw5q8BFmAzJ6eaOeCYRo0NF/8ANTH2mXjAAAA"
      },
      "Metadata": {
        "aws:cdk:path": "LambdaHTTPAPIGateway/CDKMetadata/Default"
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