from tests.utilities import TestTemplates, true, false


class TestLambdaFunction(TestTemplates):

    def test_lambda_function(self):
        self.assert_template_equal(
            'LambdaFunction',
            {
  "Resources": {
    "LambdaFunctionServiceRoleC555A460": {
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
        "aws:cdk:path": "LambdaFunction/LambdaFunction/ServiceRole/Resource"
      }
    },
    "LambdaFunctionBF21E41F": {
      "Type": "AWS::Lambda::Function",
      "Properties": {
        "Code": {
          "S3Bucket": {
            "Ref": "AssetParameters6f583a693f7945791d3a4b8a29d8b95cea3f49f5bb75a5d9dfa3e659813fcc34S3BucketE10C6C17"
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
                          "Ref": "AssetParameters6f583a693f7945791d3a4b8a29d8b95cea3f49f5bb75a5d9dfa3e659813fcc34S3VersionKeyCAE90EDD"
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
                          "Ref": "AssetParameters6f583a693f7945791d3a4b8a29d8b95cea3f49f5bb75a5d9dfa3e659813fcc34S3VersionKeyCAE90EDD"
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
            "LambdaFunctionServiceRoleC555A460",
            "Arn"
          ]
        },
        "Handler": "hello.handler",
        "Runtime": "python3.8",
        "Timeout": 60
      },
      "DependsOn": [
        "LambdaFunctionServiceRoleC555A460"
      ],
      "Metadata": {
        "aws:cdk:path": "LambdaFunction/LambdaFunction/Resource",
        "aws:asset:path": "asset.6f583a693f7945791d3a4b8a29d8b95cea3f49f5bb75a5d9dfa3e659813fcc34",
        "aws:asset:is-bundled": false,
        "aws:asset:property": "Code"
      }
    },
    "CDKMetadata": {
      "Type": "AWS::CDK::Metadata",
      "Properties": {
        "Analytics": "v2:deflate64:H4sIAAAAAAAA/zWNwQ6CMBBEv4V7WSAcvCokngl+wVpWrECbdLcxpum/SzGe5s1kdqeBpj1BXZzxzaWelipq5wniTVAv6sJMsuNs7Kx6Z1l80KL6hx3Q40ZCPpuR2AWvKfPemowYZ5PKL+OK231CiNdgdY5z589JGdwgjm49TrMmxW2JeZbhWN89dEEvJB0ypaSGjzydrVpoamiKFxtT+mDFbATjT7/XaQiA1AAAAA=="
      },
      "Metadata": {
        "aws:cdk:path": "LambdaFunction/CDKMetadata/Default"
      },
      "Condition": "CDKMetadataAvailable"
    }
  },
  "Parameters": {
    "AssetParameters6f583a693f7945791d3a4b8a29d8b95cea3f49f5bb75a5d9dfa3e659813fcc34S3BucketE10C6C17": {
      "Type": "String",
      "Description": "S3 bucket for asset \"6f583a693f7945791d3a4b8a29d8b95cea3f49f5bb75a5d9dfa3e659813fcc34\""
    },
    "AssetParameters6f583a693f7945791d3a4b8a29d8b95cea3f49f5bb75a5d9dfa3e659813fcc34S3VersionKeyCAE90EDD": {
      "Type": "String",
      "Description": "S3 key for asset version \"6f583a693f7945791d3a4b8a29d8b95cea3f49f5bb75a5d9dfa3e659813fcc34\""
    },
    "AssetParameters6f583a693f7945791d3a4b8a29d8b95cea3f49f5bb75a5d9dfa3e659813fcc34ArtifactHash70AD0F2F": {
      "Type": "String",
      "Description": "Artifact hash for asset \"6f583a693f7945791d3a4b8a29d8b95cea3f49f5bb75a5d9dfa3e659813fcc34\""
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
  },
  "Outputs": {
    "ExportsOutputFnGetAttLambdaFunctionBF21E41FArn8BD9CD14": {
      "Value": {
        "Fn::GetAtt": [
          "LambdaFunctionBF21E41F",
          "Arn"
        ]
      },
      "Export": {
        "Name": "LambdaFunction:ExportsOutputFnGetAttLambdaFunctionBF21E41FArn8BD9CD14"
      }
    }
  }
}
        )