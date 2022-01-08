from tests.utilities import TestTemplates, true, false


class TestSqsFlow(TestTemplates):

    def test_sqs_flow(self):
        self.assert_template_equal(
            'SqsFlow',
            {
  "Resources": {
    "RDSPublishQueue2BEA1A7F": {
      "Type": "AWS::SQS::Queue",
      "Properties": {
        "VisibilityTimeout": 300
      },
      "UpdateReplacePolicy": "Delete",
      "DeletionPolicy": "Delete",
      "Metadata": {
        "aws:cdk:path": "SqsFlow/RDSPublishQueue/Resource"
      }
    },
    "sqsServiceRole07D53907": {
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
      },
      "Metadata": {
        "aws:cdk:path": "SqsFlow/sqs/ServiceRole/Resource"
      }
    },
    "sqsServiceRoleDefaultPolicy6C36BFC1": {
      "Type": "AWS::IAM::Policy",
      "Properties": {
        "PolicyDocument": {
          "Statement": [
            {
              "Action": [
                "xray:PutTraceSegments",
                "xray:PutTelemetryRecords"
              ],
              "Effect": "Allow",
              "Resource": "*"
            },
            {
              "Action": [
                "sqs:SendMessage",
                "sqs:GetQueueAttributes",
                "sqs:GetQueueUrl"
              ],
              "Effect": "Allow",
              "Resource": {
                "Fn::GetAtt": [
                  "RDSPublishQueue2BEA1A7F",
                  "Arn"
                ]
              }
            }
          ],
          "Version": "2012-10-17"
        },
        "PolicyName": "sqsServiceRoleDefaultPolicy6C36BFC1",
        "Roles": [
          {
            "Ref": "sqsServiceRole07D53907"
          }
        ]
      },
      "Metadata": {
        "aws:cdk:path": "SqsFlow/sqs/ServiceRole/DefaultPolicy/Resource"
      }
    },
    "sqs1386CA46": {
      "Type": "AWS::Lambda::Function",
      "Properties": {
        "Code": {
          "S3Bucket": {
            "Ref": "AssetParameters121bd1015c718f11470ee4f7750028d48d0f96e49fef7e4751df1759cfeb6f06S3Bucket6BDF5420"
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
                          "Ref": "AssetParameters121bd1015c718f11470ee4f7750028d48d0f96e49fef7e4751df1759cfeb6f06S3VersionKey6B2E3823"
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
                          "Ref": "AssetParameters121bd1015c718f11470ee4f7750028d48d0f96e49fef7e4751df1759cfeb6f06S3VersionKey6B2E3823"
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
            "sqsServiceRole07D53907",
            "Arn"
          ]
        },
        "Environment": {
          "Variables": {
            "SQS_URL": {
              "Ref": "RDSPublishQueue2BEA1A7F"
            }
          }
        },
        "Handler": "sqs.handler",
        "Runtime": "python3.8",
        "TracingConfig": {
          "Mode": "Active"
        }
      },
      "DependsOn": [
        "sqsServiceRoleDefaultPolicy6C36BFC1",
        "sqsServiceRole07D53907"
      ],
      "Metadata": {
        "aws:cdk:path": "SqsFlow/sqs/Resource",
        "aws:asset:path": "asset.121bd1015c718f11470ee4f7750028d48d0f96e49fef7e4751df1759cfeb6f06",
        "aws:asset:is-bundled": false,
        "aws:asset:property": "Code"
      }
    },
    "sqsAllowInvokeSqsFlowSNSTopic3A729E90E75E55D8": {
      "Type": "AWS::Lambda::Permission",
      "Properties": {
        "Action": "lambda:InvokeFunction",
        "FunctionName": {
          "Fn::GetAtt": [
            "sqs1386CA46",
            "Arn"
          ]
        },
        "Principal": "sns.amazonaws.com",
        "SourceArn": {
          "Fn::ImportValue": "XRayTracer:ExportsOutputRefTheXRayTracerSnsFanOutTopicDE7E70F8D479F0D6"
        }
      },
      "Metadata": {
        "aws:cdk:path": "SqsFlow/sqs/AllowInvoke:SqsFlowSNSTopic3A729E90"
      }
    },
    "sqsSNSTopic2F92781E": {
      "Type": "AWS::SNS::Subscription",
      "Properties": {
        "Protocol": "lambda",
        "TopicArn": {
          "Fn::ImportValue": "XRayTracer:ExportsOutputRefTheXRayTracerSnsFanOutTopicDE7E70F8D479F0D6"
        },
        "Endpoint": {
          "Fn::GetAtt": [
            "sqs1386CA46",
            "Arn"
          ]
        },
        "Region": {
          "Fn::Select": [
            3,
            {
              "Fn::Split": [
                ":",
                {
                  "Fn::ImportValue": "XRayTracer:ExportsOutputRefTheXRayTracerSnsFanOutTopicDE7E70F8D479F0D6"
                }
              ]
            }
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "SqsFlow/sqs/SNSTopic/Resource"
      }
    },
    "sqssubscribeServiceRole6533E28E": {
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
      },
      "Metadata": {
        "aws:cdk:path": "SqsFlow/sqs_subscribe/ServiceRole/Resource"
      }
    },
    "sqssubscribeServiceRoleDefaultPolicyBF52038F": {
      "Type": "AWS::IAM::Policy",
      "Properties": {
        "PolicyDocument": {
          "Statement": [
            {
              "Action": [
                "xray:PutTraceSegments",
                "xray:PutTelemetryRecords"
              ],
              "Effect": "Allow",
              "Resource": "*"
            },
            {
              "Action": [
                "sqs:ReceiveMessage",
                "sqs:ChangeMessageVisibility",
                "sqs:GetQueueUrl",
                "sqs:DeleteMessage",
                "sqs:GetQueueAttributes"
              ],
              "Effect": "Allow",
              "Resource": {
                "Fn::GetAtt": [
                  "RDSPublishQueue2BEA1A7F",
                  "Arn"
                ]
              }
            }
          ],
          "Version": "2012-10-17"
        },
        "PolicyName": "sqssubscribeServiceRoleDefaultPolicyBF52038F",
        "Roles": [
          {
            "Ref": "sqssubscribeServiceRole6533E28E"
          }
        ]
      },
      "Metadata": {
        "aws:cdk:path": "SqsFlow/sqs_subscribe/ServiceRole/DefaultPolicy/Resource"
      }
    },
    "sqssubscribe6A7ED757": {
      "Type": "AWS::Lambda::Function",
      "Properties": {
        "Code": {
          "S3Bucket": {
            "Ref": "AssetParameters121bd1015c718f11470ee4f7750028d48d0f96e49fef7e4751df1759cfeb6f06S3Bucket6BDF5420"
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
                          "Ref": "AssetParameters121bd1015c718f11470ee4f7750028d48d0f96e49fef7e4751df1759cfeb6f06S3VersionKey6B2E3823"
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
                          "Ref": "AssetParameters121bd1015c718f11470ee4f7750028d48d0f96e49fef7e4751df1759cfeb6f06S3VersionKey6B2E3823"
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
            "sqssubscribeServiceRole6533E28E",
            "Arn"
          ]
        },
        "Handler": "sqs_subscribe.handler",
        "Runtime": "python3.8",
        "TracingConfig": {
          "Mode": "Active"
        }
      },
      "DependsOn": [
        "sqssubscribeServiceRoleDefaultPolicyBF52038F",
        "sqssubscribeServiceRole6533E28E"
      ],
      "Metadata": {
        "aws:cdk:path": "SqsFlow/sqs_subscribe/Resource",
        "aws:asset:path": "asset.121bd1015c718f11470ee4f7750028d48d0f96e49fef7e4751df1759cfeb6f06",
        "aws:asset:is-bundled": false,
        "aws:asset:property": "Code"
      }
    },
    "sqssubscribeSqsEventSourceSqsFlowRDSPublishQueueD1D2BBCF1DF330F8": {
      "Type": "AWS::Lambda::EventSourceMapping",
      "Properties": {
        "FunctionName": {
          "Ref": "sqssubscribe6A7ED757"
        },
        "EventSourceArn": {
          "Fn::GetAtt": [
            "RDSPublishQueue2BEA1A7F",
            "Arn"
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "SqsFlow/sqs_subscribe/SqsEventSource:SqsFlowRDSPublishQueueD1D2BBCF/Resource"
      }
    },
    "CDKMetadata": {
      "Type": "AWS::CDK::Metadata",
      "Properties": {
        "Analytics": "v2:deflate64:H4sIAAAAAAAA/2VQQU7EMAx8C/c0S9ULR9gV3FYqLR/wut7FtElKnIBWUf5OE4QE4uQZezQeu9Vtd6fbm3v4lAaneZfQedJpDICzehChsMEL24s6OCvBRwzqcLY9eDAUyBcykLjokQreVBMHdjarYpnkXXR6jhTrtIKsFjCnCXR6ihaLtox+4568YZHCHj/IhrHaH2Fda5Cz/d/NisHoNLilLqq1dwvjtRpWlJV0DZSbRNfTNq73EWcKexBSYresYzwJel5/svzhL25lLNqcs+qv4dXZXafb2+2Db8Lc+GgDG9LDd/0Cedcaol4BAAA="
      },
      "Metadata": {
        "aws:cdk:path": "SqsFlow/CDKMetadata/Default"
      },
      "Condition": "CDKMetadataAvailable"
    }
  },
  "Parameters": {
    "AssetParameters121bd1015c718f11470ee4f7750028d48d0f96e49fef7e4751df1759cfeb6f06S3Bucket6BDF5420": {
      "Type": "String",
      "Description": "S3 bucket for asset \"121bd1015c718f11470ee4f7750028d48d0f96e49fef7e4751df1759cfeb6f06\""
    },
    "AssetParameters121bd1015c718f11470ee4f7750028d48d0f96e49fef7e4751df1759cfeb6f06S3VersionKey6B2E3823": {
      "Type": "String",
      "Description": "S3 key for asset version \"121bd1015c718f11470ee4f7750028d48d0f96e49fef7e4751df1759cfeb6f06\""
    },
    "AssetParameters121bd1015c718f11470ee4f7750028d48d0f96e49fef7e4751df1759cfeb6f06ArtifactHash8CDD66AF": {
      "Type": "String",
      "Description": "Artifact hash for asset \"121bd1015c718f11470ee4f7750028d48d0f96e49fef7e4751df1759cfeb6f06\""
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