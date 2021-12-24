from tests.utilities import TestTemplates, true, false

class TestWebApplicationFirewall(TestTemplates):

    def test_web_application_firewall(self):
        self.assert_template_equal(
            'WebApplicationFirewall',
            {
  "Resources": {
    "WebACL": {
      "Type": "AWS::WAFv2::WebACL",
      "Properties": {
        "DefaultAction": {
          "Allow": {}
        },
        "Scope": "REGIONAL",
        "VisibilityConfig": {
          "CloudWatchMetricsEnabled": true,
          "MetricName": "webACL",
          "SampledRequestsEnabled": true
        },
        "Name": "HelloWorldACL",
        "Rules": [
          {
            "Name": "AWS-AWSManagedRulesCommonRuleSet",
            "OverrideAction": {
              "None": {}
            },
            "Priority": 1,
            "Statement": {
              "ManagedRuleGroupStatement": {
                "ExcludedRules": [
                  {
                    "Name": "SizeRestrictions_BODY"
                  }
                ],
                "Name": "AWSManagedRulesCommonRuleSet",
                "VendorName": "AWS"
              }
            },
            "VisibilityConfig": {
              "CloudWatchMetricsEnabled": true,
              "MetricName": "awsCommonRules",
              "SampledRequestsEnabled": true
            }
          },
          {
            "Name": "awsAnonymousIP",
            "OverrideAction": {
              "None": {}
            },
            "Priority": 2,
            "Statement": {
              "ManagedRuleGroupStatement": {
                "ExcludedRules": [],
                "Name": "AWSManagedRulesAnonymousIpList",
                "VendorName": "AWS"
              }
            },
            "VisibilityConfig": {
              "CloudWatchMetricsEnabled": true,
              "MetricName": "awsAnonymous",
              "SampledRequestsEnabled": true
            }
          },
          {
            "Name": "aws_Ipreputation",
            "OverrideAction": {
              "None": {}
            },
            "Priority": 3,
            "Statement": {
              "ManagedRuleGroupStatement": {
                "ExcludedRules": [],
                "Name": "AWSManagedRulesAmazonIpReputationList",
                "VendorName": "AWS"
              }
            },
            "VisibilityConfig": {
              "CloudWatchMetricsEnabled": true,
              "MetricName": "aws_reputation",
              "SampledRequestsEnabled": true
            }
          },
          {
            "Action": {
              "Block": {}
            },
            "Name": "geoblocking_rule",
            "Priority": 4,
            "Statement": {
              "GeoMatchStatement": {
                "CountryCodes": [
                  "NZ"
                ]
              }
            },
            "VisibilityConfig": {
              "CloudWatchMetricsEnabled": true,
              "MetricName": "geoblock",
              "SampledRequestsEnabled": true
            }
          }
        ]
      },
      "Metadata": {
        "aws:cdk:path": "WebApplicationFirewall/WebACL"
      }
    },
    "WAFAssnAPI": {
      "Type": "AWS::WAFv2::WebACLAssociation",
      "Properties": {
        "ResourceArn": {
          "Fn::Join": [
            "",
            [
              "arn:aws:apigateway:",
              {
                "Ref": "AWS::Region"
              },
              "::/restapis/",
              {
                "Fn::ImportValue": "LambdaAPIGateway:ExportsOutputRefLambdaAPIGateway527FD98828FC969E"
              },
              "/stages/",
              {
                "Fn::ImportValue": "LambdaAPIGateway:ExportsOutputRefLambdaAPIGatewayDeploymentStageprod74ACA052509E0E94"
              }
            ]
          ]
        },
        "WebACLArn": {
          "Fn::GetAtt": [
            "WebACL",
            "Arn"
          ]
        }
      },
      "Metadata": {
        "aws:cdk:path": "WebApplicationFirewall/WAFAssnAPI"
      }
    },
    "CDKMetadata": {
      "Type": "AWS::CDK::Metadata",
      "Properties": {
        "Analytics": "v2:deflate64:H4sIAAAAAAAA/z2LMQ+CMBBGfwt7OagMrpKuDgYG53qUeBJ7Se+QmIb/Lmji9L3kvc+CbY5QFye/SInDVGXkFCD36nEyjqNomlGNG2MXhOeEYedNDKTEcTX7cfHj6wB5E9dwa93Z/KkVYST/TVdzeeudY9WArcEWDyEq0xyVngG6334AZqPFo5AAAAA="
      },
      "Metadata": {
        "aws:cdk:path": "WebApplicationFirewall/CDKMetadata/Default"
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