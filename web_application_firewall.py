import aws_cdk
import constructs
import well_architected


# class WebApplicationFirewall(aws_cdk.Stack):
class WebApplicationFirewall(well_architected.WellArchitectedFrameworkStack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        target_arn=None,
        web_application_firewall_scope='REGIONAL',
        **kwargs
    ) -> None:
        '''NOTE: HTTP APIs are not supported yet'''
        super().__init__(scope, id, **kwargs)
        self.create_web_application_firewall_association(
            target_arn=target_arn,
            web_application_firewall=self.create_web_application_firewall(
                scope=web_application_firewall_scope,
                waf_rules=[
                    self.common_ruleset(),
                    self.anonymous_ip_rule(),
                    self.restricted_ip_list_rule(),
                    self.add_geoblock_rule(),
                ],
            ),
        )

    def default_override_action(self):
        return aws_cdk.aws_wafv2.CfnWebACL.OverrideActionProperty(none={})

    def create_visibility_configuration(self, metric_name):
        return aws_cdk.aws_wafv2.CfnWebACL.VisibilityConfigProperty(
            cloud_watch_metrics_enabled=True,
            metric_name=metric_name,
            sampled_requests_enabled=True
        )

    def create_managed_rule(self, name=None, priority=None, excluded_rules=None):
        return aws_cdk.aws_wafv2.CfnWebACL.RuleProperty(
            name=name,
            priority=priority,
            override_action=self.default_override_action(),
            visibility_config=self.create_visibility_configuration(name),
            statement=aws_cdk.aws_wafv2.CfnWebACL.StatementProperty(
                managed_rule_group_statement=aws_cdk.aws_wafv2.CfnWebACL.ManagedRuleGroupStatementProperty(
                    name=name,
                    vendor_name='AWS',
                    excluded_rules=excluded_rules if excluded_rules else []
                )
            ),
        )

    def common_ruleset(self):
        return self.create_managed_rule(
            name='AWSManagedRulesCommonRuleSet',
            priority=1,
            excluded_rules=[
                aws_cdk.aws_wafv2.CfnWebACL.ExcludedRuleProperty(
                    name='SizeRestrictions_BODY'
                )
            ],
        )

    def anonymous_ip_rule(self):
        return self.create_managed_rule(
            name='AWSManagedRulesAnonymousIpList',
            priority=2,
        )

    def restricted_ip_list_rule(self):
        return self.create_managed_rule(
            name='AWSManagedRulesAmazonIpReputationList',
            priority=3,
        )

    def add_geoblock_rule(self):
        return aws_cdk.aws_wafv2.CfnWebACL.RuleProperty(
            name='geoblocking_rule',
            priority=4,
            action=aws_cdk.aws_wafv2.CfnWebACL.RuleActionProperty(block={}),
            visibility_config=self.create_visibility_configuration('geoblock'),
            statement=aws_cdk.aws_wafv2.CfnWebACL.StatementProperty(
                geo_match_statement=aws_cdk.aws_wafv2.CfnWebACL.GeoMatchStatementProperty(
                    country_codes=['NZ'],
                )
            ),
        )

    def allow_action(self):
        return aws_cdk.aws_wafv2.CfnWebACL.DefaultActionProperty(allow={})

    def create_web_application_firewall(self, waf_rules=None, scope=None):
        return aws_cdk.aws_wafv2.CfnWebACL(
            self, 'WebACL',
            default_action=self.allow_action(),
            scope=scope,
            visibility_config=self.create_visibility_configuration('webACL'),
            name='WebApplicationFirewall',
            rules=waf_rules
        )

    def create_web_application_firewall_association(self, web_application_firewall=None, target_arn=None):
        return aws_cdk.aws_wafv2.CfnWebACLAssociation(
            self, 'WAFAPIGatewayAssociation',
            web_acl_arn=web_application_firewall.attr_arn,
            resource_arn=target_arn
        )