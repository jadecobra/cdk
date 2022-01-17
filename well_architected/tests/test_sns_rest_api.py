from tests.utilities import TestTemplates, true, false


class TestXRayTracer(TestTemplates):

    def test_xray_tracer(self):
        self.assert_template_equal(
            'SnsRestApi',
            {
  "Resources": {
    "RestApi0C43BF4B": {
      "Type": "AWS::ApiGateway::RestApi",
      "Properties": {
        "Name": "RestApi"
      },
      "Metadata": {
        "aws:cdk:path": "SnsRestApi/RestApi/Resource"
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
      },
      "Metadata": {
        "aws:cdk:path": "SnsRestApi/RestApi/CloudWatchRole/Resource"
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
      ],
      "Metadata": {
        "aws:cdk:path": "SnsRestApi/RestApi/Account"
      }
    },
    "RestApiDeployment180EC50353456d9ae36c41aab4342990e922625e": {
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
      ],
      "Metadata": {
        "aws:cdk:path": "SnsRestApi/RestApi/Deployment/Resource"
      }
    },
    "RestApiDeploymentStageprod3855DE66": {
      "Type": "AWS::ApiGateway::Stage",
      "Properties": {
        "RestApiId": {
          "Ref": "RestApi0C43BF4B"
        },
        "DeploymentId": {
          "Ref": "RestApiDeployment180EC50353456d9ae36c41aab4342990e922625e"
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
      ],
      "Metadata": {
        "aws:cdk:path": "SnsRestApi/RestApi/DeploymentStage.prod/Resource"
      }
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
      },
      "Metadata": {
        "aws:cdk:path": "SnsRestApi/RestApi/Default/GET/Resource"
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
      },
      "Metadata": {
        "aws:cdk:path": "SnsRestApi/RestApi/Default/{proxy+}/Resource"
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
      },
      "Metadata": {
        "aws:cdk:path": "SnsRestApi/RestApi/Default/{proxy+}/GET/Resource"
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
      },
      "Metadata": {
        "aws:cdk:path": "SnsRestApi/RestApi/ResponseModel/Resource"
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
      },
      "Metadata": {
        "aws:cdk:path": "SnsRestApi/RestApi/ErrorResponseModel/Resource"
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
      },
      "Metadata": {
        "aws:cdk:path": "SnsRestApi/ApiGatewaySNSRole/Resource"
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
      },
      "Metadata": {
        "aws:cdk:path": "SnsRestApi/ApiGatewaySNSRole/DefaultPolicy/Resource"
      }
    },
    "CDKMetadata": {
      "Type": "AWS::CDK::Metadata",
      "Properties": {
        "Analytics": "v2:deflate64:H4sIAAAAAAAA/02OSw7CMAxEz8I+BKqu2AFli0Bwgig1xdDGVeOoiqrcnaQf1JWf7fF4MpnlB7nfHFVvt7r87gZNHcjhyUp/RfEyN8etY1GQsdw5zWn2AEuu05A4LkpkJBNEshhUi5Vi6JWXQ9TxqcX5ZMGT1uQMiwu0NfkGzOi56uLvavSeYPl2VhbEFfhNZVrOtM7y5yuVUI+iBEGgamIaqidVqneqUfvUThRCEHcfHc0ul9leZpuPRdx2MSg2IB9T/QEEFiXVLgEAAA=="
      },
      "Metadata": {
        "aws:cdk:path": "SnsRestApi/CDKMetadata/Default"
      },
      "Condition": "CDKMetadataAvailable"
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