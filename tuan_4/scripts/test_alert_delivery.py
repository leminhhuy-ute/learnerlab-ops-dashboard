"""Run pending/confirmed SNS delivery checks on the isolated Week 3 Lambda.

The product alert configuration and billing records are never modified. Email
is read without echo and is excluded from saved evidence and stdout.
"""

import argparse
import datetime as dt
from decimal import Decimal
import getpass
import hashlib
import io
import json
from pathlib import Path
import urllib.request
import zipfile

import boto3
from boto3.dynamodb.conditions import Key

ACCOUNT = "213858341631"
REGION = "us-east-1"
FUNCTION = "learnerlab-ops-week3-threshold-negative-test"
PRODUCT = "learnerlab-ops-week2-threshold-alert"
TOPIC = f"arn:aws:sns:{REGION}:{ACCOUNT}:learnerlab-ops-week3-negative-test"
TABLE = "learnerlab-ops-week2-snapshots"
REPLAY_TABLE = "learnerlab-ops-week4-billing-replay-test"
# Historical data replay only: product remains at its 48-hour limit.
REPLAY_MAX_AGE_HOURS = 336
OUT = Path.home() / "week4-final-20261023"


def stamp():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def save(name, value):
    value = {"checkedAtUtc": stamp(), **value}
    (OUT / name).write_text(json.dumps(value, indent=2), encoding="utf-8")
    print(json.dumps(value))


def subscriptions(sns):
    return [s for p in sns.get_paginator("list_subscriptions_by_topic").paginate(TopicArn=TOPIC) for s in p["Subscriptions"]]


def counts(sns):
    subs = subscriptions(sns)
    return {"confirmed": sum(s["SubscriptionArn"] not in {"PendingConfirmation", "Deleted"} for s in subs),
            "pending": sum(s["SubscriptionArn"] == "PendingConfirmation" for s in subs)}


def product_env(lam):
    config = lam.get_function_configuration(FunctionName=PRODUCT)
    env = config["Environment"]["Variables"]
    assert env["ALERT_THRESHOLD_USD"] == "10"
    assert env.get("MAX_SNAPSHOT_AGE_HOURS", "48") == "48"
    assert env["TOPIC_ARN"] == f"arn:aws:sns:{REGION}:{ACCOUNT}:learnerlab-ops-week2-alerts"
    return env


def prepare(lam, sns, source):
    before = product_env(lam)
    ddb = boto3.resource("dynamodb", region_name=REGION)
    query = {"KeyConditionExpression": Key("PK").eq("BILLING#" + ACCOUNT) & Key("SK").begins_with("SNAPSHOT#"), "ScanIndexForward": False}
    items = []
    while True:
        page = ddb.Table(TABLE).query(**query)
        items.extend(page.get("Items", []))
        if "LastEvaluatedKey" not in page:
            break
        query["ExclusiveStartKey"] = page["LastEvaluatedKey"]
    candidates = [x for x in items if x.get("status") == "ok" and Decimal(str(x.get("total", 0))) > 0
        and 0 <= (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(x["collectedAt"].replace("Z", "+00:00"))).total_seconds() <= REPLAY_MAX_AGE_HOURS * 3600]
    assert candidates, "No positive real billing snapshot inside the explicit historical replay window"
    item = candidates[0]
    amount = Decimal(str(item["total"]))
    client = boto3.client("dynamodb", region_name=REGION)
    assert REPLAY_TABLE not in client.list_tables()["TableNames"], "Replay table already exists; inspect it before rerunning"
    client.create_table(TableName=REPLAY_TABLE, BillingMode="PAY_PER_REQUEST",
        KeySchema=[{"AttributeName":"PK","KeyType":"HASH"},{"AttributeName":"SK","KeyType":"RANGE"}],
        AttributeDefinitions=[{"AttributeName":"PK","AttributeType":"S"},{"AttributeName":"SK","AttributeType":"S"}],
        Tags=[{"Key":"Project","Value":"learnerlab-ops"},{"Key":"Owner","Value":"24110019"},{"Key":"Purpose","Value":"week4-disposable-billing-replay"}])
    client.get_waiter("table_exists").wait(TableName=REPLAY_TABLE)
    ddb.Table(REPLAY_TABLE).put_item(Item=item)
    assert ddb.Table(REPLAY_TABLE).get_item(Key={"PK":item["PK"],"SK":item["SK"]},ConsistentRead=True)["Item"] == item
    config = lam.get_function_configuration(FunctionName=FUNCTION)
    tags = lam.list_tags(Resource=config["FunctionArn"])["Tags"]
    assert tags.get("Project") == "learnerlab-ops" and tags.get("Owner") == "24110019"
    backup = OUT / "alert-test-before.json"
    if not backup.exists():
        backup.write_text(json.dumps({"environment": config["Environment"]["Variables"]}, indent=2))
    code = source.read_bytes()
    deployed = lam.get_function(FunctionName=FUNCTION)
    old_zip = urllib.request.urlopen(deployed["Code"]["Location"]).read()
    old_source = zipfile.ZipFile(io.BytesIO(old_zip)).read("lambda_function.py")
    (OUT / "alert-test-before.zip").write_bytes(old_zip)
    if code != old_source:
        package = io.BytesIO()
        with zipfile.ZipFile(package, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("lambda_function.py", code)
        lam.update_function_code(FunctionName=FUNCTION, ZipFile=package.getvalue(), RevisionId=config["RevisionId"])
        lam.get_waiter("function_updated_v2").wait(FunctionName=FUNCTION)
    config = lam.get_function_configuration(FunctionName=FUNCTION)
    env = {**config["Environment"]["Variables"], "TABLE_NAME": REPLAY_TABLE, "TOPIC_ARN": TOPIC,
           "ACCOUNT_ID": ACCOUNT, "ALERT_THRESHOLD_USD": str(amount / 2), "MAX_SNAPSHOT_AGE_HOURS": str(REPLAY_MAX_AGE_HOURS)}
    lam.update_function_configuration(FunctionName=FUNCTION, Environment={"Variables": env}, RevisionId=config["RevisionId"])
    lam.get_waiter("function_updated_v2").wait(FunctionName=FUNCTION)
    save("alert-plan.json", {"snapshotId": item["SK"], "collectedAt": item["collectedAt"],
         "withinHistoricalReplayWindow": True, "estimated": bool(item.get("estimated", True)),
         "replayMaxAgeHours": REPLAY_MAX_AGE_HOURS, "productMaxAgeHours": 48,
         "sourceSnapshotWithinProduct48Hours": (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(item["collectedAt"].replace("Z", "+00:00"))).total_seconds() <= 48 * 3600,
         "sourceTable": TABLE, "isolatedReplayTable": REPLAY_TABLE, "replayItemMatchesSource": True,
         "selectedSnapshotIsLatest": item["SK"] == items[0]["SK"],
         "periodStart": item.get("periodStart"), "periodEndExclusive": item.get("periodEndExclusive"),
         "thresholdMethod": "one half of the positive real snapshot amount, test Lambda only",
         "sourceSha256": hashlib.sha256(code).hexdigest(), "productEnvironmentUnchanged": before == product_env(lam)})
    email = getpass.getpass("Recipient email for the isolated test (not echoed): ").strip()
    assert "@" in email and "\n" not in email
    existing = [s for s in subscriptions(sns) if s.get("Protocol") == "email" and s.get("Endpoint") == email]
    if not existing:
        sns.subscribe(TopicArn=TOPIC, Protocol="email", Endpoint=email)
    save("alert-subscription-state.json", {**counts(sns), "confirmationRequested": not bool(existing)})


def invoke(lam, sns, phase):
    result_file = OUT / f"alert-{phase}-result.json"
    if result_file.exists():
        raise RuntimeError("This phase already has evidence; inspect it instead of resending")
    current = counts(sns)
    if phase == "pending":
        assert current["confirmed"] == 0 and current["pending"] > 0
    else:
        assert current["confirmed"] > 0, "Confirm the test-topic subscription first"
    before = product_env(lam)
    response = lam.invoke(FunctionName=FUNCTION, Payload=b"{}")
    raw = json.loads(response["Payload"].read())
    safe = {k: raw[k] for k in ("status", "published", "messageId", "confirmedSubscriptionCount",
            "pendingSubscriptionCount", "snapshotId", "collectedAt", "snapshotAgeSeconds", "maxSnapshotAgeHours") if k in raw}
    safe.update({"lambdaStatusCode": response["StatusCode"], "functionError": response.get("FunctionError"),
                 "usedNormalThresholdBranch": True, "productEnvironmentUnchanged": before == product_env(lam)})
    if "amountUsd" in raw and "thresholdUsd" in raw:
        safe["realAmountStrictlyExceedsTestThreshold"] = Decimal(raw["amountUsd"]) > Decimal(raw["thresholdUsd"])
    save(result_file.name, safe)
    assert response["StatusCode"] == 200 and not response.get("FunctionError")
    assert safe.get("realAmountStrictlyExceedsTestThreshold") is True
    if phase == "pending":
        assert raw["status"] == "sns_subscription_pending_confirmation" and raw["published"] is False and "messageId" not in raw
    else:
        assert raw["status"] == "alert_published" and raw["published"] is True and raw.get("messageId")


def restore(lam):
    before = product_env(lam)
    config = lam.get_function_configuration(FunctionName=FUNCTION)
    env = {**config["Environment"]["Variables"], "ALERT_THRESHOLD_USD": "10", "MAX_SNAPSHOT_AGE_HOURS": "48", "TOPIC_ARN": TOPIC, "TABLE_NAME": TABLE}
    lam.update_function_configuration(FunctionName=FUNCTION, Environment={"Variables": env}, RevisionId=config["RevisionId"])
    lam.get_waiter("function_updated_v2").wait(FunctionName=FUNCTION)
    now = lam.get_function_configuration(FunctionName=FUNCTION)["Environment"]["Variables"]
    client = boto3.client("dynamodb", region_name=REGION)
    table = client.describe_table(TableName=REPLAY_TABLE)["Table"]
    tags = {t["Key"]:t["Value"] for t in client.list_tags_of_resource(ResourceArn=table["TableArn"])["Tags"]}
    assert tags.get("Purpose") == "week4-disposable-billing-replay" and tags.get("Owner") == "24110019"
    client.delete_table(TableName=REPLAY_TABLE)
    client.get_waiter("table_not_exists").wait(TableName=REPLAY_TABLE)
    save("alert-test-safe-config.json", {"testThresholdResetTo10": now["ALERT_THRESHOLD_USD"] == "10",
         "testTableRestored": now["TABLE_NAME"] == TABLE, "replayTableDeleted": True,
         "testTopicStillIsolated": now["TOPIC_ARN"] == TOPIC, "productEnvironmentUnchanged": before == product_env(lam)})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "pending", "positive", "restore"))
    parser.add_argument("--source", type=Path, default=Path("/tmp/week4-threshold.py"))
    args = parser.parse_args()
    assert boto3.client("sts", region_name=REGION).get_caller_identity()["Account"] == ACCOUNT
    OUT.mkdir(exist_ok=True)
    lambda_client = boto3.client("lambda", region_name=REGION)
    sns_client = boto3.client("sns", region_name=REGION)
    if args.phase == "prepare":
        prepare(lambda_client, sns_client, args.source)
    elif args.phase == "restore":
        restore(lambda_client)
    else:
        invoke(lambda_client, sns_client, args.phase)
