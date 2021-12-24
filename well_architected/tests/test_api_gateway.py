from tests.utilities import TestTemplates, true, false


class TestAPIGateway(TestTemplates):

    def log_group(self):
      return {
        "helloAPILogs01DC10B3": {
          "Type": "AWS::Logs::LogGroup",
          "Properties": {
            "RetentionInDays": 731
          },
          "UpdateReplacePolicy": "Retain",
          "DeletionPolicy": "Retain",
          "Metadata": {
            "aws:cdk:path": "LambdaAPIGateway/helloAPILogs/Resource"
          }
        }
      }

    def iam_role_for_cloudwatch(self):
      return {
        "LambdaAPIGatewayCloudWatchRoleA621D6AA": {
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
            "aws:cdk:path": "LambdaAPIGateway/LambdaAPIGateway/CloudWatchRole/Resource"
          }
        }
      }

    def rest_api(self):
      return {
        "LambdaAPIGateway527FD988": {
          "Type": "AWS::ApiGateway::RestApi",
          "Properties": {
            "EndpointConfiguration": {
              "Types": [
                "REGIONAL"
              ]
            },
            "Name": "hello"
          },
          "Metadata": {
            "aws:cdk:path": "LambdaAPIGateway/LambdaAPIGateway/Resource"
          }
        }
      }

    def api_gateway_account(self):
      return {
        "LambdaAPIGatewayAccount80C6550F": {
          "Type": "AWS::ApiGateway::Account",
          "Properties": {
            "CloudWatchRoleArn": {
              "Fn::GetAtt": [
                "LambdaAPIGatewayCloudWatchRoleA621D6AA",
                "Arn"
              ]
            }
          },
          "DependsOn": [
            "LambdaAPIGateway527FD988"
          ],
          "Metadata": {
            "aws:cdk:path": "LambdaAPIGateway/LambdaAPIGateway/Account"
          }
        }
      }

    def api_gateway_deployment(self):
      return {
        "LambdaAPIGatewayDeploymentE937914C0356969e891f453d30de932d4de61531": {
          "Type": "AWS::ApiGateway::Deployment",
          "Properties": {
            "RestApiId": {
              "Ref": "LambdaAPIGateway527FD988"
            },
            "Description": "Automatically created by the RestApi construct"
          },
          "DependsOn": [
            "LambdaAPIGatewayhelloGET71776088",
            "LambdaAPIGatewayhello24FCF180"
          ],
          "Metadata": {
            "aws:cdk:path": "LambdaAPIGateway/LambdaAPIGateway/Deployment/Resource"
          }
        }
      }

    def api_gateway_deployment_stage(self):
      return {
        "LambdaAPIGatewayDeploymentStageprod74ACA052": {
          "Type": "AWS::ApiGateway::Stage",
          "Properties": {
            "RestApiId": {
              "Ref": "LambdaAPIGateway527FD988"
            },
            "AccessLogSetting": {
              "DestinationArn": {
                "Fn::GetAtt": [
                  "helloAPILogs01DC10B3",
                  "Arn"
                ]
              },
              "Format": "$context.identity.sourceIp $context.identity.caller $context.identity.user [$context.requestTime] \"$context.httpMethod $context.resourcePath $context.protocol\" $context.status $context.responseLength $context.requestId"
            },
            "DeploymentId": {
              "Ref": "LambdaAPIGatewayDeploymentE937914C0356969e891f453d30de932d4de61531"
            },
            "MethodSettings": [
              {
                "DataTraceEnabled": false,
                "HttpMethod": "*",
                "ResourcePath": "/*",
                "ThrottlingBurstLimit": 200,
                "ThrottlingRateLimit": 100
              }
            ],
            "StageName": "prod"
          },
          "DependsOn": [
            "LambdaAPIGatewayAccount80C6550F"
          ],
          "Metadata": {
            "aws:cdk:path": "LambdaAPIGateway/LambdaAPIGateway/DeploymentStage.prod/Resource"
          }
        }
      }

    def api_gateway_resource(self):
      return {
        "LambdaAPIGatewayhello24FCF180": {
          "Type": "AWS::ApiGateway::Resource",
          "Properties": {
            "ParentId": {
              "Fn::GetAtt": [
                "LambdaAPIGateway527FD988",
                "RootResourceId"
              ]
            },
            "PathPart": "hello",
            "RestApiId": {
              "Ref": "LambdaAPIGateway527FD988"
            }
          },
          "Metadata": {
            "aws:cdk:path": "LambdaAPIGateway/LambdaAPIGateway/Default/hello/Resource"
          }
        }
      }

    def lambda_resource_policy(self):
      return {
        
      }

    def test_api_gateway(self):
        self.assert_template_equal(
            'LambdaAPIGateway',
            {
              "Resources": {
                **self.log_group(),
                **self.rest_api(),
                **self.iam_role_for_cloudwatch(),
                **self.api_gateway_account(),
                **self.api_gateway_deployment(),
                **self.api_gateway_deployment_stage(),
                **self.api_gateway_resource(),
                "LambdaAPIGatewayhelloGETApiPermissionLambdaAPIGateway52B24D07GEThello3B63010E": {
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
                            "Ref": "LambdaAPIGateway527FD988"
                          },
                          "/",
                          {
                            "Ref": "LambdaAPIGatewayDeploymentStageprod74ACA052"
                          },
                          "/GET/hello"
                        ]
                      ]
                    }
                  },
                  "Metadata": {
                    "aws:cdk:path": "LambdaAPIGateway/LambdaAPIGateway/Default/hello/GET/ApiPermission.LambdaAPIGateway52B24D07.GET..hello"
                  }
                },
                "LambdaAPIGatewayhelloGETApiPermissionTestLambdaAPIGateway52B24D07GEThello6B64019C": {
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
                            "Ref": "LambdaAPIGateway527FD988"
                          },
                          "/test-invoke-stage/GET/hello"
                        ]
                      ]
                    }
                  },
                  "Metadata": {
                    "aws:cdk:path": "LambdaAPIGateway/LambdaAPIGateway/Default/hello/GET/ApiPermission.Test.LambdaAPIGateway52B24D07.GET..hello"
                  }
                },
                "LambdaAPIGatewayhelloGET71776088": {
                  "Type": "AWS::ApiGateway::Method",
                  "Properties": {
                    "HttpMethod": "GET",
                    "ResourceId": {
                      "Ref": "LambdaAPIGatewayhello24FCF180"
                    },
                    "RestApiId": {
                      "Ref": "LambdaAPIGateway527FD988"
                    },
                    "AuthorizationType": "NONE",
                    "Integration": {
                      "IntegrationHttpMethod": "POST",
                      "IntegrationResponses": [
                        {
                          "ResponseParameters": {
                            "method.response.header.Access-Control-Allow-Origin": "'*'"
                          },
                          "StatusCode": "200"
                        }
                      ],
                      "Type": "AWS",
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
                              "Fn::ImportValue": "LambdaFunction:ExportsOutputFnGetAttLambdaFunctionBF21E41FArn8BD9CD14"
                            },
                            "/invocations"
                          ]
                        ]
                      }
                    },
                    "MethodResponses": [
                      {
                        "ResponseParameters": {
                          "method.response.header.Access-Control-Allow-Origin": true
                        },
                        "StatusCode": "200"
                      }
                    ]
                  },
                  "Metadata": {
                    "aws:cdk:path": "LambdaAPIGateway/LambdaAPIGateway/Default/hello/GET/Resource"
                  }
                },
                "CDKMetadata": {
                  "Type": "AWS::CDK::Metadata",
                  "Properties": {
                    "Analytics": "v2:deflate64:H4sIAAAAAAAA/1VPQW7CMBB8C3ezEHHoFUqlXloVwQuMs6RbYq9lr4UiK3/HJo1aTjuzHs/MNtBsXmC92OpbXJr2usqGA0I+iTZXtb+4ryQ+idqzixKSkbo7YuQUDFZcHloSYjeqapF77iLkD+7eAydfFTMuAk+dFrzpAXLxkJ2nX7sZ7ozh5ES9oe95sOgeef9Y6dU9cicwN3nV8Y88VfxE+ea2riY0KtK2xHM/6cocVa/tudVQ+AGDpRjrPaM6DOWHW22gWUOz+IlEy1DakUU4TvMOxk3XjD8BAAA="
                  },
                  "Metadata": {
                    "aws:cdk:path": "LambdaAPIGateway/CDKMetadata/Default"
                  },
                  "Condition": "CDKMetadataAvailable"
                }
              },
              "Outputs": {
                "LambdaAPIGatewayEndpoint5DC258E1": {
                  "Value": {
                    "Fn::Join": [
                      "",
                      [
                        "https://",
                        {
                          "Ref": "LambdaAPIGateway527FD988"
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
                          "Ref": "LambdaAPIGatewayDeploymentStageprod74ACA052"
                        },
                        "/"
                      ]
                    ]
                  }
                },
                "ExportsOutputRefLambdaAPIGateway527FD98828FC969E": {
                  "Value": {
                    "Ref": "LambdaAPIGateway527FD988"
                  },
                  "Export": {
                    "Name": "LambdaAPIGateway:ExportsOutputRefLambdaAPIGateway527FD98828FC969E"
                  }
                },
                "ExportsOutputRefLambdaAPIGatewayDeploymentStageprod74ACA052509E0E94": {
                  "Value": {
                    "Ref": "LambdaAPIGatewayDeploymentStageprod74ACA052"
                  },
                  "Export": {
                    "Name": "LambdaAPIGateway:ExportsOutputRefLambdaAPIGatewayDeploymentStageprod74ACA052509E0E94"
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