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
        "Name": "WebApplicationFirewall",
        "Rules": [
          {
            "Name": "AWSManagedRulesCommonRuleSet",
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
              "MetricName": "AWSManagedRulesCommonRuleSet",
              "SampledRequestsEnabled": true
            }
          },
          {
            "Name": "AWSManagedRulesAnonymousIpList",
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
              "MetricName": "AWSManagedRulesAnonymousIpList",
              "SampledRequestsEnabled": true
            }
          },
          {
            "Name": "AWSManagedRulesAmazonIpReputationList",
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
              "MetricName": "AWSManagedRulesAmazonIpReputationList",
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
      }
    },
    "WAFAPIGatewayAssociation": {
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
                "Fn::ImportValue": "LambdaRestAPIGateway:ExportsOutputRefLambdaAPIGateway527FD98828FC969E"
              },
              "/stages/",
              {
                "Fn::ImportValue": "LambdaRestAPIGateway:ExportsOutputRefLambdaAPIGatewayDeploymentStageprod74ACA052509E0E94"
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
      }
    }
  }
}
        )