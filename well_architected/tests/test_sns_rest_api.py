from tests.utilities import TestTemplates, true, false


class TestXRayTracer(TestTemplates):

    def test_sns_rest_api(self):
        self.assert_template_equal(
            'SnsRestApi',
            {
  "Resources": {
    "RestApi0C43BF4B": {
      "Type": "AWS::ApiGateway::RestApi",
      "Properties": {
        "Name": "RestApi"
      }
    },
    "RestApiCloudWatchRoleE3ED6605": {
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
    "RestApiAccount7C83CF5A": {
      "Type": "AWS::ApiGateway::Account",
      "Properties": {
        "CloudWatchRoleArn": {
          "Fn::GetAtt": [
            "RestApiCloudWatchRoleE3ED6605",
            "Arn"
          ]
        }
      },
      "DependsOn": [
        "RestApi0C43BF4B"
      ]
    },
    "RestApiDeployment180EC50310ca31bc7c64b136e655b95e390d9332": {
      "Type": "AWS::ApiGateway::Deployment",
      "Properties": {
        "RestApiId": {
          "Ref": "RestApi0C43BF4B"
        },
        "Description": "Automatically created by the RestApi construct"
      },
      "DependsOn": [
        "RestApiproxyGET3EA512AF",
        "RestApiproxyC95856DD",
        "RestApiGET0F59260B",
        "RestApiErrorResponseModelA6C9DD94",
        "RestApiResponseModel056B6183"
      ]
    },
    "RestApiDeploymentStageprod3855DE66": {
      "Type": "AWS::ApiGateway::Stage",
      "Properties": {
        "RestApiId": {
          "Ref": "RestApi0C43BF4B"
        },
        "DeploymentId": {
          "Ref": "RestApiDeployment180EC50310ca31bc7c64b136e655b95e390d9332"
        },
        "MethodSettings": [
          {
            "DataTraceEnabled": true,
            "HttpMethod": "*",
            "LoggingLevel": "INFO",
            "MetricsEnabled": true,
            "ResourcePath": "/*"
          }
        ],
        "StageName": "prod",
        "TracingEnabled": true
      },
      "DependsOn": [
        "RestApiAccount7C83CF5A"
      ]
    },
    "RestApiGET0F59260B": {
      "Type": "AWS::ApiGateway::Method",
      "Properties": {
        "HttpMethod": "GET",
        "ResourceId": {
          "Fn::GetAtt": [
            "RestApi0C43BF4B",
            "RootResourceId"
          ]
        },
        "RestApiId": {
          "Ref": "RestApi0C43BF4B"
        },
        "AuthorizationType": "NONE",
        "Integration": {
          "Credentials": {
            "Fn::GetAtt": [
              "ApiGatewaySNSRole1BAAAE75",
              "Arn"
            ]
          },
          "IntegrationHttpMethod": "POST",
          "IntegrationResponses": [
            {
              "ResponseTemplates": {
                "application/json": "{\"message\": \"message added to topic\"}"
              },
              "StatusCode": "200"
            },
            {
              "ResponseParameters": {
                "method.response.header.Content-Type": "'application/json'",
                "method.response.header.Access-Control-Allow-Origin": "'*'",
                "method.response.header.Access-Control-Allow-Credentials": "'true'"
              },
              "ResponseTemplates": {
                "application/json": "{\"state\":\"error\",\"message\":\"$util.escapeJavaScript($input.path('$.errorMessage'))\"}"
              },
              "SelectionPattern": "^\\[Error\\].*",
              "StatusCode": "400"
            }
          ],
          "PassthroughBehavior": "NEVER",
          "RequestParameters": {
            "integration.request.header.Content-Type": "'application/x-www-form-urlencoded'"
          },
          "RequestTemplates": {
            "application/json": {
              "Fn::Join": [
                "",
                [
                  "Action=Publish&TargetArn=$util.urlEncode('",
                  {
                    "Fn::ImportValue": "XRayTracerSnsFanOutTopic:ExportsOutputRefXRayTracerSnsFanOutTopic129D23A131FFD088"
                  },
                  "')&Message=$util.urlEncode($context.path)&Version=2010-03-31"
                ]
              ]
            }
          },
          "Type": "AWS",
          "Uri": {
            "Fn::Join": [
              "",
              [
                "arn:aws:apigateway:",
                {
                  "Ref": "AWS::Region"
                },
                ":sns:path//"
              ]
            ]
          }
        },
        "MethodResponses": [
          {
            "ResponseModels": {
              "application/json": {
                "Ref": "RestApiResponseModel056B6183"
              }
            },
            "ResponseParameters": {
              "method.response.header.Content-Type": true,
              "method.response.header.Access-Control-Allow-Origin": true,
              "method.response.header.Access-Control-Allow-Credentials": true
            },
            "StatusCode": "200"
          },
          {
            "ResponseModels": {
              "application/json": {
                "Ref": "RestApiErrorResponseModelA6C9DD94"
              }
            },
            "ResponseParameters": {
              "method.response.header.Content-Type": true,
              "method.response.header.Access-Control-Allow-Origin": true,
              "method.response.header.Access-Control-Allow-Credentials": true
            },
            "StatusCode": "400"
          }
        ]
      }
    },
    "RestApiproxyC95856DD": {
      "Type": "AWS::ApiGateway::Resource",
      "Properties": {
        "ParentId": {
          "Fn::GetAtt": [
            "RestApi0C43BF4B",
            "RootResourceId"
          ]
        },
        "PathPart": "{proxy+}",
        "RestApiId": {
          "Ref": "RestApi0C43BF4B"
        }
      }
    },
    "RestApiproxyGET3EA512AF": {
      "Type": "AWS::ApiGateway::Method",
      "Properties": {
        "HttpMethod": "GET",
        "ResourceId": {
          "Ref": "RestApiproxyC95856DD"
        },
        "RestApiId": {
          "Ref": "RestApi0C43BF4B"
        },
        "AuthorizationType": "NONE",
        "Integration": {
          "Credentials": {
            "Fn::GetAtt": [
              "ApiGatewaySNSRole1BAAAE75",
              "Arn"
            ]
          },
          "IntegrationHttpMethod": "POST",
          "IntegrationResponses": [
            {
              "ResponseTemplates": {
                "application/json": "{\"message\": \"message added to topic\"}"
              },
              "StatusCode": "200"
            },
            {
              "ResponseParameters": {
                "method.response.header.Content-Type": "'application/json'",
                "method.response.header.Access-Control-Allow-Origin": "'*'",
                "method.response.header.Access-Control-Allow-Credentials": "'true'"
              },
              "ResponseTemplates": {
                "application/json": "{\"state\":\"error\",\"message\":\"$util.escapeJavaScript($input.path('$.errorMessage'))\"}"
              },
              "SelectionPattern": "^\\[Error\\].*",
              "StatusCode": "400"
            }
          ],
          "PassthroughBehavior": "NEVER",
          "RequestParameters": {
            "integration.request.header.Content-Type": "'application/x-www-form-urlencoded'"
          },
          "RequestTemplates": {
            "application/json": {
              "Fn::Join": [
                "",
                [
                  "Action=Publish&TargetArn=$util.urlEncode('",
                  {
                    "Fn::ImportValue": "XRayTracerSnsFanOutTopic:ExportsOutputRefXRayTracerSnsFanOutTopic129D23A131FFD088"
                  },
                  "')&Message=$util.urlEncode($context.path)&Version=2010-03-31"
                ]
              ]
            }
          },
          "Type": "AWS",
          "Uri": {
            "Fn::Join": [
              "",
              [
                "arn:aws:apigateway:",
                {
                  "Ref": "AWS::Region"
                },
                ":sns:path//"
              ]
            ]
          }
        },
        "MethodResponses": [
          {
            "ResponseModels": {
              "application/json": {
                "Ref": "RestApiResponseModel056B6183"
              }
            },
            "ResponseParameters": {
              "method.response.header.Content-Type": true,
              "method.response.header.Access-Control-Allow-Origin": true,
              "method.response.header.Access-Control-Allow-Credentials": true
            },
            "StatusCode": "200"
          },
          {
            "ResponseModels": {
              "application/json": {
                "Ref": "RestApiErrorResponseModelA6C9DD94"
              }
            },
            "ResponseParameters": {
              "method.response.header.Content-Type": true,
              "method.response.header.Access-Control-Allow-Origin": true,
              "method.response.header.Access-Control-Allow-Credentials": true
            },
            "StatusCode": "400"
          }
        ]
      }
    },
    "RestApiResponseModel056B6183": {
      "Type": "AWS::ApiGateway::Model",
      "Properties": {
        "RestApiId": {
          "Ref": "RestApi0C43BF4B"
        },
        "ContentType": "application/json",
        "Name": "ResponseModel",
        "Schema": {
          "properties": {
            "message": {
              "type": "string"
            }
          },
          "$schema": "http://json-schema.org/draft-04/schema#",
          "title": "pollResponse",
          "type": "object"
        }
      }
    },
    "RestApiErrorResponseModelA6C9DD94": {
      "Type": "AWS::ApiGateway::Model",
      "Properties": {
        "RestApiId": {
          "Ref": "RestApi0C43BF4B"
        },
        "ContentType": "application/json",
        "Name": "ErrorResponseModel",
        "Schema": {
          "properties": {
            "message": {
              "type": "string"
            },
            "state": {
              "type": "string"
            }
          },
          "$schema": "http://json-schema.org/draft-04/schema#",
          "title": "errorResponse",
          "type": "object"
        }
      }
    },
    "ApiGatewaySNSRole1BAAAE75": {
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
        }
      }
    },
    "ApiGatewaySNSRoleDefaultPolicyCA5D0260": {
      "Type": "AWS::IAM::Policy",
      "Properties": {
        "PolicyDocument": {
          "Statement": [
            {
              "Action": "sns:Publish",
              "Effect": "Allow",
              "Resource": {
                "Fn::ImportValue": "XRayTracerSnsFanOutTopic:ExportsOutputRefXRayTracerSnsFanOutTopic129D23A131FFD088"
              }
            }
          ],
          "Version": "2012-10-17"
        },
        "PolicyName": "ApiGatewaySNSRoleDefaultPolicyCA5D0260",
        "Roles": [
          {
            "Ref": "ApiGatewaySNSRole1BAAAE75"
          }
        ]
      }
    }
  },
  "Outputs": {
    "RestApiEndpoint0551178A": {
      "Value": {
        "Fn::Join": [
          "",
          [
            "https://",
            {
              "Ref": "RestApi0C43BF4B"
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
              "Ref": "RestApiDeploymentStageprod3855DE66"
            },
            "/"
          ]
        ]
      }
    }
  }
}
        )