"""Read-only, sanitized Week 4 security/dependency review in AWS CloudShell.

Uses the current Learner Lab session; never prints credentials, email endpoints,
presigned URLs, cost values, or arbitrary Lambda environment variables.
"""

import datetime
import json

import boto3
from botocore.exceptions import ClientError


ACCOUNT = "213858341631"
REGION = "us-east-1"
PREFIX = "learnerlab-ops-"
TEST_FUNCTION = "learnerlab-ops-week3-threshold-negative-test"
API_ID = "qvpnt8h5yh"
MISSING = {"ResourceNotFoundException", "ResourceNotFound", "NoSuchBucketPolicy", "NoSuchTagSet"}


def optional(call, **kwargs):
    try:
        return call(**kwargs)
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        if code in MISSING:
            return None
        raise


def collect():
    account = boto3.client("sts", region_name=REGION).get_caller_identity()["Account"]
    if account != ACCOUNT:
        raise RuntimeError("Wrong AWS account; review stopped")
    report = {"checkedAtUtc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "account": account}
    s3 = boto3.client("s3", region_name=REGION)
    buckets = []
    for bucket in s3.list_buckets()["Buckets"]:
        name = bucket["Name"]
        if not name.startswith(PREFIX):
            continue
        location = s3.get_bucket_location(Bucket=name).get("LocationConstraint") or "us-east-1"
        if location not in {"us-east-1", "us-west-2"}:
            raise RuntimeError("Project bucket outside allowed Regions")
        policy = optional(s3.get_bucket_policy_status, Bucket=name)
        acl = s3.get_bucket_acl(Bucket=name)["Grants"]
        buckets.append({
            "name": name, "region": location,
            "publicAccessBlock": s3.get_public_access_block(Bucket=name)["PublicAccessBlockConfiguration"],
            "encryption": [r["ApplyServerSideEncryptionByDefault"]["SSEAlgorithm"] for r in s3.get_bucket_encryption(Bucket=name)["ServerSideEncryptionConfiguration"]["Rules"]],
            "isPublicPolicy": policy["PolicyStatus"]["IsPublic"] if policy else False,
            "hasBucketPolicy": policy is not None,
            "publicAclGrantCount": sum(g["Grantee"].get("URI", "").endswith(("/AllUsers", "/AuthenticatedUsers")) for g in acl),
            "tags": {t["Key"]: t["Value"] for t in s3.get_bucket_tagging(Bucket=name)["TagSet"] if t["Key"] in {"Project", "Owner", "Environment"}},
        })
    report["buckets"] = buckets
    api = boto3.client("apigatewayv2", region_name=REGION)
    report["apiRoutes"] = [{k: r.get(k) for k in ("RouteKey", "AuthorizationType", "Target")} for r in api.get_routes(ApiId=API_ID)["Items"]]
    report["apiStages"] = [{k: s.get(k) for k in ("StageName", "AutoDeploy")} for s in api.get_stages(ApiId=API_ID)["Items"]]
    lam = boto3.client("lambda", region_name=REGION)
    functions = []
    for page in lam.get_paginator("list_functions").paginate():
        for function in page["Functions"]:
            name = function["FunctionName"]
            if not name.startswith(PREFIX):
                continue
            urls = lam.list_function_url_configs(FunctionName=name).get("FunctionUrlConfigs", [])
            policy = optional(lam.get_policy, FunctionName=name)
            statements = json.loads(policy["Policy"]).get("Statement", []) if policy else []
            functions.append({
                "name": name, "role": function["Role"].split("/")[-1],
                "functionUrlCount": len(urls),
                "functionUrlAuthTypes": [url["AuthType"] for url in urls],
                "invokePolicy": [{k: s.get(k) for k in ("Effect", "Principal", "Action", "Condition")} for s in statements],
            })
    report["functions"] = functions
    events = boto3.client("events", region_name=REGION)
    rules = []
    for page in events.get_paginator("list_rules").paginate(NamePrefix=PREFIX):
        for rule in page["Rules"]:
            targets = events.list_targets_by_rule(Rule=rule["Name"])["Targets"]
            rules.append({"name": rule["Name"], "state": rule["State"], "targetArns": [t["Arn"] for t in targets]})
    report["rules"] = rules
    report["testEventSourceMappings"] = [{k: m.get(k) for k in ("State", "EventSourceArn")} for m in lam.list_event_source_mappings(FunctionName=TEST_FUNCTION)["EventSourceMappings"]]
    sns = boto3.client("sns", region_name=REGION)
    topics = []
    for page in sns.get_paginator("list_topics").paginate():
        for topic in page["Topics"]:
            arn = topic["TopicArn"]
            if not arn.split(":")[-1].startswith(PREFIX):
                continue
            subscriptions = []
            for sub_page in sns.get_paginator("list_subscriptions_by_topic").paginate(TopicArn=arn):
                subscriptions.extend(sub_page["Subscriptions"])
            policy = json.loads(sns.get_topic_attributes(TopicArn=arn)["Attributes"].get("Policy", "{}"))
            topics.append({
                "name": arn.split(":")[-1],
                "confirmed": sum(s["SubscriptionArn"] not in {"PendingConfirmation", "Deleted"} for s in subscriptions),
                "pending": sum(s["SubscriptionArn"] == "PendingConfirmation" for s in subscriptions),
                "policy": [{k: s.get(k) for k in ("Effect", "Principal", "Action", "Condition")} for s in policy.get("Statement", [])],
            })
    report["topics"] = topics
    cw = boto3.client("cloudwatch", region_name=REGION)
    report["alarms"] = [{k: a.get(k) for k in ("AlarmName", "StateValue", "AlarmActions", "OKActions", "InsufficientDataActions", "Dimensions")} for a in cw.describe_alarms(AlarmNamePrefix=PREFIX)["MetricAlarms"]]
    logs = boto3.client("logs", region_name=REGION)
    report["testLogGroups"] = [{k: g.get(k) for k in ("logGroupName", "retentionInDays", "storedBytes")} for g in logs.describe_log_groups(logGroupNamePrefix=f"/aws/lambda/{TEST_FUNCTION}")["logGroups"]]
    report["west2ProjectFunctionCount"] = sum(f["FunctionName"].startswith(PREFIX) for page in boto3.client("lambda", region_name="us-west-2").get_paginator("list_functions").paginate() for f in page["Functions"])
    return report


if __name__ == "__main__":
    print(json.dumps(collect(), ensure_ascii=False, separators=(",", ":")))
