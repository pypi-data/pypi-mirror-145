
import json

from cdktf_cdktf_provider_aws.cloudfront import (
    CloudfrontDistribution,
    CloudfrontDistributionOriginS3OriginConfig,
    CloudfrontDistributionOrigin,
    CloudfrontDistributionCustomErrorResponse,
    CloudfrontOriginAccessIdentity,
    CloudfrontDistributionCustomErrorResponse,
    CloudfrontDistributionDefaultCacheBehavior,
    CloudfrontDistributionDefaultCacheBehaviorForwardedValues,
    CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookies,
    CloudfrontDistributionRestrictions,
    CloudfrontDistributionRestrictionsGeoRestriction,
    CloudfrontDistributionViewerCertificate,
)
from cdktf_cdktf_provider_aws.wafv2 import DataAwsWafv2WebAcl
from cdktf_cdktf_provider_aws.s3 import (
    S3Bucket,
    S3BucketPolicy,
    S3BucketObject,
    S3BucketPublicAccessBlock,
)
from cdktf_cdktf_provider_aws.iam import (
    DataAwsIamPolicyDocumentStatement,
    DataAwsIamPolicyDocument,
    DataAwsIamPolicyDocumentStatementPrincipals,
)
from cdktf_cdktf_provider_aws.route53 import Route53Record


def create_web_site(
    stack,
    name,
    web_config,
    fqdn,
    web_acl_name,
    zone_id,
    global_provider,
    acm_cert,
):
    origin_access_identity = CloudfrontOriginAccessIdentity(
        stack,
        id=f"{name}_origin_access_identity",
        comment=f"OAI For {fqdn}",
    )

    site_bucket = S3Bucket(
        stack, id=f"{name}_site_bucket", bucket=fqdn, acl="private")

    S3BucketPublicAccessBlock(
        stack,
        id=f"{name}_site_bucket_public_access_block",
        bucket=site_bucket.id,
        block_public_acls=True,
        block_public_policy=True,
        restrict_public_buckets=True,
        ignore_public_acls=True,
    )

    s3_object_access = DataAwsIamPolicyDocumentStatement(
        sid="s3ObjectAccess",
        actions=["s3:GetObject"],
        resources=[f"{site_bucket.arn}/*"],
        effect="Allow",
        principals=[
            DataAwsIamPolicyDocumentStatementPrincipals(
                type="AWS",
                identifiers=[origin_access_identity.iam_arn],
            )
        ],
    )

    s3_list_bucket_access = DataAwsIamPolicyDocumentStatement(
        sid="s3ListBucketAccess",
        actions=["s3:ListBucket"],
        resources=[site_bucket.arn],
        effect="Allow",
        principals=[
            DataAwsIamPolicyDocumentStatementPrincipals(
                type="AWS",
                identifiers=[origin_access_identity.iam_arn],
            )
        ],
    )

    config = json.dumps(web_config)

    S3BucketObject(
        stack,
        id=f"{name}_site_config",
        bucket=site_bucket.bucket,
        key="config.js",
        content=f"window.env = Object.assign({{}}, window.env, {config})",
    )

    policy_document = DataAwsIamPolicyDocument(
        stack,
        id=f"{name}_site_bucket_policy_document",
        statement=[s3_object_access, s3_list_bucket_access],
    )

    S3BucketPolicy(
        stack,
        id=f"{name}_site_bucket_policy",
        bucket=site_bucket.id,
        policy=policy_document.json,
    )

    waf_acl = DataAwsWafv2WebAcl(
        stack,
        id=f"{name}_web_wafv2_acl",
        name=web_acl_name,
        scope="CLOUDFRONT",
        provider=global_provider,
    )

    cloud_front_dist = CloudfrontDistribution(
        stack,
        id=f"{name}_cloudfront_dist",
        enabled=True,
        is_ipv6_enabled=True,
        comment=f"Cloudfront distribution for {fqdn}",
        default_root_object="index.html",
        price_class="PriceClass_100",
        web_acl_id=waf_acl.arn,
        origin=[
            CloudfrontDistributionOrigin(
                domain_name=site_bucket.bucket_regional_domain_name,
                origin_id=f"{site_bucket.id}-origin",
                s3_origin_config=CloudfrontDistributionOriginS3OriginConfig(
                    origin_access_identity=origin_access_identity.cloudfront_access_identity_path
                ),
            )
        ],
        custom_error_response=[
            CloudfrontDistributionCustomErrorResponse(
                error_caching_min_ttl=300,
                error_code=404,
                response_code=200,
                response_page_path="/index.html",
            )
        ],
        aliases=[fqdn],
        default_cache_behavior=CloudfrontDistributionDefaultCacheBehavior(
            min_ttl=0,
            default_ttl=0,
            max_ttl=0,
            target_origin_id=f"{site_bucket.id}-origin",
            viewer_protocol_policy="redirect-to-https",
            allowed_methods=["GET", "HEAD"],
            cached_methods=["GET", "HEAD"],
            forwarded_values=CloudfrontDistributionDefaultCacheBehaviorForwardedValues(
                query_string=False,
                cookies=CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookies(
                    forward="none",
                ),
            ),
        ),
        restrictions=CloudfrontDistributionRestrictions(
            geo_restriction=CloudfrontDistributionRestrictionsGeoRestriction(
                restriction_type="whitelist",
                locations=["GB", "IE"],
            )
        ),
        viewer_certificate=CloudfrontDistributionViewerCertificate(
            acm_certificate_arn=acm_cert.arn,
            ssl_support_method="sni-only",
            minimum_protocol_version="TLSv1.2_2018",
        ),
    )

    Route53Record(
        stack,
        id=f"{name}_site_route_53_record",
        zone_id=zone_id,
        name=fqdn,
        type="CNAME",
        ttl=300,
        records=[cloud_front_dist.domain_name],
    )
