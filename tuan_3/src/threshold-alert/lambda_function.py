"""Week 3 candidate: fail closed when an SNS topic has no confirmed endpoint.

This copy is prepared for review and local testing. It has not yet been
deployed to AWS Learner Lab.
"""

from decimal import Decimal
import json
import os


def _subscription_counts(sns, topic_arn):
    """Return confirmed and pending subscription counts without exposing endpoints."""
    confirmed = 0
    pending = 0
    paginator = sns.get_paginator("list_subscriptions_by_topic")
    for page in paginator.paginate(TopicArn=topic_arn):
        for subscription in page.get("Subscriptions", []):
            arn = subscription.get("SubscriptionArn", "")
            if arn == "PendingConfirmation":
                pending += 1
            elif arn and arn != "Deleted":
                confirmed += 1
    return confirmed, pending


def _publish_or_skip(sns, topic_arn, subject, message):
    confirmed, pending = _subscription_counts(sns, topic_arn)
    if confirmed == 0:
        status = (
            "sns_subscription_pending_confirmation"
            if pending
            else "sns_no_confirmed_subscribers"
        )
        return {
            "status": status,
            "published": False,
            "confirmedSubscriptionCount": confirmed,
            "pendingSubscriptionCount": pending,
        }

    result = sns.publish(TopicArn=topic_arn, Subject=subject, Message=message)
    status = "alert_published_with_pending_subscriptions" if pending else "alert_published"
    return {
        "status": status,
        "published": True,
        "messageId": result["MessageId"],
        "confirmedSubscriptionCount": confirmed,
        "pendingSubscriptionCount": pending,
    }


def _evaluate_billing_item(item, sns, topic_arn, threshold):
    if item.get("status") != "ok":
        return {
            "status": "billing_snapshot_not_ok",
            "published": False,
            "snapshotId": item.get("SK"),
        }

    amount = Decimal(str(item.get("total", "0")))
    details = {
        "periodStart": item.get("periodStart"),
        "periodEndExclusive": item.get("periodEndExclusive"),
        "estimated": bool(item.get("estimated", True)),
        "amountUsd": str(amount),
        "thresholdUsd": str(threshold),
        "snapshotId": item.get("SK"),
    }
    if amount < threshold:
        return {"status": "below_threshold", "published": False, **details}

    publish_result = _publish_or_skip(
        sns,
        topic_arn,
        "Learner Lab estimated cost threshold reached",
        json.dumps(details, ensure_ascii=False),
    )
    return {**publish_result, **details}


def lambda_handler(event, context):
    """Read the newest billing snapshot and publish only when delivery is possible."""
    import boto3
    from boto3.dynamodb.conditions import Key

    event = event or {}
    table_name = os.environ["TABLE_NAME"]
    topic_arn = os.environ["TOPIC_ARN"]
    account_id = os.environ["ACCOUNT_ID"]
    threshold = Decimal(os.environ.get("ALERT_THRESHOLD_USD", "10"))
    region = os.environ.get("AWS_REGION", "us-east-1")

    ddb = boto3.resource("dynamodb", region_name=region).Table(table_name)
    sns = boto3.client("sns", region_name=region)

    if event.get("test") is True:
        message = "SNS integration test for learnerlab-ops-week2-alerts. This is not a cost alert."
        return _publish_or_skip(
            sns, topic_arn, "Learner Lab SNS integration test", message
        )

    response = ddb.query(
        KeyConditionExpression=Key("PK").eq("BILLING#" + account_id),
        ScanIndexForward=False,
        Limit=1,
    )
    items = response.get("Items", [])
    if not items:
        return {"status": "no_billing_snapshot", "published": False}

    return _evaluate_billing_item(items[0], sns, topic_arn, threshold)
