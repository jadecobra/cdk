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
    "WebserviceIntegrationLambdaHandlerServiceRole851361F8": {
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
    "WebserviceIntegrationLambdaHandlerServiceRoleDefaultPolicy86CA93C2": {
      "Type": "AWS::IAM::Policy",
      "Properties": {
        "PolicyDocument": {
          "Statement": [
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
        "PolicyName": "WebserviceIntegrationLambdaHandlerServiceRoleDefaultPolicy86CA93C2",
        "Roles": [
          {
            "Ref": "WebserviceIntegrationLambdaHandlerServiceRole851361F8"
          }
        ]
      }
    },
    "WebserviceIntegrationLambdaHandler5E349AB7": {
      "Type": "AWS::Lambda::Function",
      "Properties": {
        "Code": {
          "S3Bucket": {
            "Ref": "AssetParameters29c7041f179d7eacf7135df9f3e561732409c5c845f8b6c4e050e095045f1fabS3Bucket023E261A"
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
                          "Ref": "AssetParameters29c7041f179d7eacf7135df9f3e561732409c5c845f8b6c4e050e095045f1fabS3VersionKey18D81FFC"
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
                          "Ref": "AssetParameters29c7041f179d7eacf7135df9f3e561732409c5c845f8b6c4e050e095045f1fabS3VersionKey18D81FFC"
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
            "WebserviceIntegrationLambdaHandlerServiceRole851361F8",
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
        "Runtime": "nodejs12.x",
        "Timeout": 20
      },
      "DependsOn": [
        "WebserviceIntegrationLambdaHandlerServiceRoleDefaultPolicy86CA93C2",
        "WebserviceIntegrationLambdaHandlerServiceRole851361F8"
      ]
    },
    "ErrorLambdaHandlerServiceRole5D9F8D61": {
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
    "ErrorLambdaHandlerServiceRoleDefaultPolicy9B079F8F": {
      "Type": "AWS::IAM::Policy",
      "Properties": {
        "PolicyDocument": {
          "Statement": [
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
        "PolicyName": "ErrorLambdaHandlerServiceRoleDefaultPolicy9B079F8F",
        "Roles": [
          {
            "Ref": "ErrorLambdaHandlerServiceRole5D9F8D61"
          }
        ]
      }
    },
    "ErrorLambdaHandler4224322A": {
      "Type": "AWS::Lambda::Function",
      "Properties": {
        "Code": {
          "S3Bucket": {
            "Ref": "AssetParameters34999e271a6c0000ac59864501d50f7e791b73ebf11a0fe74d22aa36992ad318S3BucketCF4F15BD"
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
                          "Ref": "AssetParameters34999e271a6c0000ac59864501d50f7e791b73ebf11a0fe74d22aa36992ad318S3VersionKeyFAF1B9D9"
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
                          "Ref": "AssetParameters34999e271a6c0000ac59864501d50f7e791b73ebf11a0fe74d22aa36992ad318S3VersionKeyFAF1B9D9"
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
            "ErrorLambdaHandlerServiceRole5D9F8D61",
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
        "Runtime": "nodejs12.x",
        "Timeout": 3
      },
      "DependsOn": [
        "ErrorLambdaHandlerServiceRoleDefaultPolicy9B079F8F",
        "ErrorLambdaHandlerServiceRole5D9F8D61"
      ]
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
                "ErrorLambdaHandler4224322A",
                "Arn"
              ]
            },
            "Id": "Target0"
          }
        ]
      }
    },
    "webserviceErrorRuleAllowEventRuleEventBridgeCircuitBreakerErrorLambdaHandlerA8CD32416274079E": {
      "Type": "AWS::Lambda::Permission",
      "Properties": {
        "Action": "lambda:InvokeFunction",
        "FunctionName": {
          "Fn::GetAtt": [
            "ErrorLambdaHandler4224322A",
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
    "CircuitBreakerGatewayDeployment9F2A82FA03c8db7cfac50ac8e7bc582f0945bb30": {
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
          "Ref": "CircuitBreakerGatewayDeployment9F2A82FA03c8db7cfac50ac8e7bc582f0945bb30"
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
            "WebserviceIntegrationLambdaHandler5E349AB7",
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
            "WebserviceIntegrationLambdaHandler5E349AB7",
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
                    "WebserviceIntegrationLambdaHandler5E349AB7",
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
            "WebserviceIntegrationLambdaHandler5E349AB7",
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
            "WebserviceIntegrationLambdaHandler5E349AB7",
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
                    "WebserviceIntegrationLambdaHandler5E349AB7",
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
    "AssetParameters29c7041f179d7eacf7135df9f3e561732409c5c845f8b6c4e050e095045f1fabS3Bucket023E261A": {
      "Type": "String",
      "Description": "S3 bucket for asset \"29c7041f179d7eacf7135df9f3e561732409c5c845f8b6c4e050e095045f1fab\""
    },
    "AssetParameters29c7041f179d7eacf7135df9f3e561732409c5c845f8b6c4e050e095045f1fabS3VersionKey18D81FFC": {
      "Type": "String",
      "Description": "S3 key for asset version \"29c7041f179d7eacf7135df9f3e561732409c5c845f8b6c4e050e095045f1fab\""
    },
    "AssetParameters29c7041f179d7eacf7135df9f3e561732409c5c845f8b6c4e050e095045f1fabArtifactHashB251200E": {
      "Type": "String",
      "Description": "Artifact hash for asset \"29c7041f179d7eacf7135df9f3e561732409c5c845f8b6c4e050e095045f1fab\""
    },
    "AssetParameters34999e271a6c0000ac59864501d50f7e791b73ebf11a0fe74d22aa36992ad318S3BucketCF4F15BD": {
      "Type": "String",
      "Description": "S3 bucket for asset \"34999e271a6c0000ac59864501d50f7e791b73ebf11a0fe74d22aa36992ad318\""
    },
    "AssetParameters34999e271a6c0000ac59864501d50f7e791b73ebf11a0fe74d22aa36992ad318S3VersionKeyFAF1B9D9": {
      "Type": "String",
      "Description": "S3 key for asset version \"34999e271a6c0000ac59864501d50f7e791b73ebf11a0fe74d22aa36992ad318\""
    },
    "AssetParameters34999e271a6c0000ac59864501d50f7e791b73ebf11a0fe74d22aa36992ad318ArtifactHashC24B1592": {
      "Type": "String",
      "Description": "Artifact hash for asset \"34999e271a6c0000ac59864501d50f7e791b73ebf11a0fe74d22aa36992ad318\""
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