from cdktf_cdktf_provider_aws.wafv2 import (
    Wafv2WebAcl,
    Wafv2WebAclDefaultAction,
    Wafv2WebAclRule,
    Wafv2WebAclDefaultActionBlock,
    Wafv2WebAclRuleAction,
    Wafv2WebAclRuleActionAllow,
    Wafv2WebAclRuleStatement,
    Wafv2WebAclRuleVisibilityConfig,
    Wafv2WebAclVisibilityConfig,
    Wafv2WebAclRuleStatementIpSetReferenceStatement,
    Wafv2IpSet
)


def cloudfront_waf(stack, web_acl_name, rules, aws_global_provider):
    return Wafv2WebAcl(
        stack,
        id=web_acl_name,
        name=web_acl_name,
        scope="CLOUDFRONT",
        default_action=Wafv2WebAclDefaultAction(
            block=Wafv2WebAclDefaultActionBlock()
        ),
        rule=rules,
        visibility_config=Wafv2WebAclVisibilityConfig(
            cloudwatch_metrics_enabled=False,
            metric_name=web_acl_name,
            sampled_requests_enabled=False),
        provider=aws_global_provider)


def global_wafv2_ip_allow_rule(stack, cidrs, aws_global_provider):
    home_ip_set = Wafv2IpSet(
        stack,
        id="home",
        name="IPSetHome",
        scope="CLOUDFRONT",
        ip_address_version="IPV4",
        addresses=cidrs,
        provider=aws_global_provider
    )

    rule = Wafv2WebAclRule(
        name="rule-1",
        priority=1,
        action=Wafv2WebAclRuleAction(
            allow=Wafv2WebAclRuleActionAllow()),
        statement=Wafv2WebAclRuleStatement(
            ip_set_reference_statement=Wafv2WebAclRuleStatementIpSetReferenceStatement(
                arn=home_ip_set.arn)
        ),
        visibility_config=Wafv2WebAclRuleVisibilityConfig(
            cloudwatch_metrics_enabled=False,
            metric_name="friendly-rule-metric-name",
            sampled_requests_enabled=False
        ),
    )

    return rule
