from tests.utilities import TestTemplates, true, false


class TestXRayTracer(TestTemplates):

    def test_xray_tracer(self):
        self.assert_template_equal(
            'XRayTracer',
            {
  "Resources": {
    "TheXRayTracerSnsFanOutTopicDE7E70F8": {
      "Type": "AWS::SNS::Topic",
      "Properties": {
        "DisplayName": "The XRay Tracer Fan Out Topic"
      },
      "Metadata": {
        "aws:cdk:path": "XRayTracer/TheXRayTracerSnsFanOutTopic/Resource"
      }
    },
    "xrayTracerAPIA84CAE80": {
      "Type": "AWS::ApiGateway::RestApi",
      "Properties": {
        "Name": "xrayTracerAPI"
      },
      "Metadata": {
        "aws:cdk:path": "XRayTracer/xrayTracerAPI/Resource"
      }
    },
    "xrayTracerAPICloudWatchRoleCCB113F4": {
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
        "aws:cdk:path": "XRayTracer/xrayTracerAPI/CloudWatchRole/Resource"
      }
    },
    "xrayTracerAPIAccount092EDE74": {
      "Type": "AWS::ApiGateway::Account",
      "Properties": {
        "CloudWatchRoleArn": {
          "Fn::GetAtt": [
            "xrayTracerAPICloudWatchRoleCCB113F4",
            "Arn"
          ]
        }
      },
      "DependsOn": [
        "xrayTracerAPIA84CAE80"
      ],
      "Metadata": {
        "aws:cdk:path": "XRayTracer/xrayTracerAPI/Account"
      }
    },
    "xrayTracerAPIDeploymentB3CB89A046a929035b39f548d29a9fe1fc0faafe": {
      "Type": "AWS::ApiGateway::Deployment",
      "Properties": {
        "RestApiId": {
          "Ref": "xrayTracerAPIA84CAE80"
        },
        "Description": "Automatically created by the RestApi construct"
      },
      "DependsOn": [
        "xrayTracerAPIproxyGET4E348609",
        "xrayTracerAPIproxy719DA214",
        "xrayTracerAPIGET7490A366",
        "xrayTracerAPIErrorResponseModel24719E91",
        "xrayTracerAPIResponseModel2591E14E"
      ],
      "Metadata": {
        "aws:cdk:path": "XRayTracer/xrayTracerAPI/Deployment/Resource"
      }
    },
    "xrayTracerAPIDeploymentStageprod85442A48": {
      "Type": "AWS::ApiGateway::Stage",
      "Properties": {
        "RestApiId": {
          "Ref": "xrayTracerAPIA84CAE80"
        },
        "DeploymentId": {
          "Ref": "xrayTracerAPIDeploymentB3CB89A046a929035b39f548d29a9fe1fc0faafe"
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
        "xrayTracerAPIAccount092EDE74"
      ],
      "Metadata": {
        "aws:cdk:path": "XRayTracer/xrayTracerAPI/DeploymentStage.prod/Resource"
      }
    },
    "xrayTracerAPIGET7490A366": {
      "Type": "AWS::ApiGateway::Method",
      "Properties": {
        "HttpMethod": "GET",
        "ResourceId": {
          "Fn::GetAtt": [
            "xrayTracerAPIA84CAE80",
            "RootResourceId"
          ]
        },
        "RestApiId": {
          "Ref": "xrayTracerAPIA84CAE80"
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
                    "Ref": "TheXRayTracerSnsFanOutTopicDE7E70F8"
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
                "Ref": "xrayTracerAPIResponseModel2591E14E"
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
                "Ref": "xrayTracerAPIErrorResponseModel24719E91"
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
        "aws:cdk:path": "XRayTracer/xrayTracerAPI/Default/GET/Resource"
      }
    },
    "xrayTracerAPIproxy719DA214": {
      "Type": "AWS::ApiGateway::Resource",
      "Properties": {
        "ParentId": {
          "Fn::GetAtt": [
            "xrayTracerAPIA84CAE80",
            "RootResourceId"
          ]
        },
        "PathPart": "{proxy+}",
        "RestApiId": {
          "Ref": "xrayTracerAPIA84CAE80"
        }
      },
      "Metadata": {
        "aws:cdk:path": "XRayTracer/xrayTracerAPI/Default/{proxy+}/Resource"
      }
    },
    "xrayTracerAPIproxyGET4E348609": {
      "Type": "AWS::ApiGateway::Method",
      "Properties": {
        "HttpMethod": "GET",
        "ResourceId": {
          "Ref": "xrayTracerAPIproxy719DA214"
        },
        "RestApiId": {
          "Ref": "xrayTracerAPIA84CAE80"
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
                    "Ref": "TheXRayTracerSnsFanOutTopicDE7E70F8"
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
                "Ref": "xrayTracerAPIResponseModel2591E14E"
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
                "Ref": "xrayTracerAPIErrorResponseModel24719E91"
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
        "aws:cdk:path": "XRayTracer/xrayTracerAPI/Default/{proxy+}/GET/Resource"
      }
    },
    "xrayTracerAPIResponseModel2591E14E": {
      "Type": "AWS::ApiGateway::Model",
      "Properties": {
        "RestApiId": {
          "Ref": "xrayTracerAPIA84CAE80"
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
        "aws:cdk:path": "XRayTracer/xrayTracerAPI/ResponseModel/Resource"
      }
    },
    "xrayTracerAPIErrorResponseModel24719E91": {
      "Type": "AWS::ApiGateway::Model",
      "Properties": {
        "RestApiId": {
          "Ref": "xrayTracerAPIA84CAE80"
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
        "aws:cdk:path": "XRayTracer/xrayTracerAPI/ErrorResponseModel/Resource"
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
        "aws:cdk:path": "XRayTracer/ApiGatewaySNSRole/Resource"
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
                "Ref": "TheXRayTracerSnsFanOutTopicDE7E70F8"
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
        "aws:cdk:path": "XRayTracer/ApiGatewaySNSRole/DefaultPolicy/Resource"
      }
    },
    "CDKMetadata": {
      "Type": "AWS::CDK::Metadata",
      "Properties": {
        "Analytics": "v2:deflate64:H4sIAAAAAAAA/02QSw7CMAxEz8I+BCo2LPltEQi4QOQaMLRx1DhCVZS7k7SAWPnZ44xHqXS1WOpqsjIvP4X6OYvAHep4FgNPtb3aQxAXRG3ZeukCSJmd0HPoAAtnoSYhtkkVi+it1/HCjqCoA2TF0c0IvkyvY34sa0cfny+uAThYUTt0Dfct2uHQX5cD3YaDI3wjbIxHtUe5c13ED/0H/PGea2yGpQJJkWlzGm7GrVKP3BD0pR0ppaSOfXa0s4Wu5vmbHp5o2uWg1KI+jfUNWRozkkMBAAA="
      },
      "Metadata": {
        "aws:cdk:path": "XRayTracer/CDKMetadata/Default"
      },
      "Condition": "CDKMetadataAvailable"
    }
  },
  "Outputs": {
    "xrayTracerAPIEndpointA106537B": {
      "Value": {
        "Fn::Join": [
          "",
          [
            "https://",
            {
              "Ref": "xrayTracerAPIA84CAE80"
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
              "Ref": "xrayTracerAPIDeploymentStageprod85442A48"
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