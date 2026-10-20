import importlib.util
import pathlib
import unittest
from datetime import datetime, timedelta, timezone


SOURCE = pathlib.Path(__file__).parents[1] / "src" / "threshold-alert" / "lambda_function.py"
SPEC = importlib.util.spec_from_file_location("week3_threshold_alert", SOURCE)
ALERT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ALERT)


class FakePaginator:
    def __init__(self, pages):
        self.pages = pages

    def paginate(self, **kwargs):
        return iter(self.pages)


class FakeSNS:
    def __init__(self, subscriptions, pages=None, list_error=None):
        self.subscriptions = subscriptions
        self.pages = pages
        self.list_error = list_error
        self.published = []
        self.paginator_requested = False

    def get_paginator(self, operation):
        if operation != "list_subscriptions_by_topic":
            raise AssertionError(f"Unexpected paginator: {operation}")
        self.paginator_requested = True
        if self.list_error:
            raise self.list_error
        return FakePaginator(self.pages or [{"Subscriptions": self.subscriptions}])

    def publish(self, **kwargs):
        self.published.append(kwargs)
        return {"MessageId": "test-message-id"}


def billing_item(total="12.50"):
    return {
        "PK": "BILLING#test-account",
        "SK": "SNAPSHOT#20261019T000000Z",
        "status": "ok",
        "total": total,
        "periodStart": "2026-10-01",
        "periodEndExclusive": "2026-10-19",
        "estimated": True,
        "collectedAt": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
    }


class ThresholdAlertTests(unittest.TestCase):
    def test_over_threshold_pending_only_does_not_publish(self):
        sns = FakeSNS(
            [{"Protocol": "email", "SubscriptionArn": "PendingConfirmation"}]
        )

        result = ALERT._evaluate_billing_item(
            billing_item(), sns, "arn:aws:sns:us-east-1:000000000000:test-topic", 10
        )

        self.assertEqual(result["status"], "sns_subscription_pending_confirmation")
        self.assertFalse(result["published"])
        self.assertEqual(result["pendingSubscriptionCount"], 1)
        self.assertEqual(sns.published, [])

    def test_over_threshold_confirmed_subscription_publishes(self):
        sns = FakeSNS(
            [{"Protocol": "email", "SubscriptionArn": "arn:confirmed-subscription"}]
        )

        result = ALERT._evaluate_billing_item(
            billing_item(), sns, "arn:aws:sns:us-east-1:000000000000:test-topic", 10
        )

        self.assertEqual(result["status"], "alert_published")
        self.assertTrue(result["published"])
        self.assertEqual(len(sns.published), 1)

    def test_over_threshold_mixed_subscriptions_reports_pending_recipient(self):
        sns = FakeSNS(
            [
                {"Protocol": "email", "SubscriptionArn": "arn:confirmed-subscription"},
                {"Protocol": "email", "SubscriptionArn": "PendingConfirmation"},
            ]
        )

        result = ALERT._evaluate_billing_item(
            billing_item(), sns, "arn:aws:sns:us-east-1:000000000000:test-topic", 10
        )

        self.assertEqual(result["status"], "alert_published_with_pending_subscriptions")
        self.assertTrue(result["published"])
        self.assertEqual(result["pendingSubscriptionCount"], 1)
        self.assertEqual(len(sns.published), 1)

    def test_below_threshold_does_not_query_or_publish(self):
        sns = FakeSNS([])

        result = ALERT._evaluate_billing_item(
            billing_item("9.99"), sns, "arn:aws:sns:us-east-1:000000000000:test-topic", 10
        )

        self.assertEqual(result["status"], "below_threshold")
        self.assertFalse(result["published"])
        self.assertFalse(sns.paginator_requested)
        self.assertEqual(sns.published, [])

    def test_stale_snapshot_fails_closed_before_sns_lookup(self):
        item = billing_item()
        item["collectedAt"] = "2026-10-13T02:00:42Z"
        sns = FakeSNS([])

        result = ALERT._evaluate_billing_item(
            item,
            sns,
            "arn:aws:sns:us-east-1:000000000000:test-topic",
            10,
            max_age_hours=48,
            now=datetime(2026, 10, 20, 6, 21, 41, tzinfo=timezone.utc),
        )

        self.assertEqual(result["status"], "stale_billing_snapshot")
        self.assertFalse(result["published"])
        self.assertEqual(result["snapshotId"], "SNAPSHOT#20261019T000000Z")
        self.assertFalse(sns.paginator_requested)
        self.assertEqual(sns.published, [])

    def test_missing_snapshot_timestamp_fails_closed(self):
        item = billing_item()
        del item["collectedAt"]
        sns = FakeSNS([])

        result = ALERT._evaluate_billing_item(
            item, sns, "arn:aws:sns:us-east-1:000000000000:test-topic", 10
        )

        self.assertEqual(result["status"], "billing_snapshot_timestamp_missing")
        self.assertFalse(result["published"])
        self.assertFalse(sns.paginator_requested)
        self.assertEqual(sns.published, [])

    def test_snapshot_exactly_at_age_limit_is_accepted(self):
        now = datetime(2026, 10, 20, 6, 21, 41, tzinfo=timezone.utc)
        item = billing_item("9.99")
        item["collectedAt"] = (now - timedelta(hours=48)).isoformat().replace("+00:00", "Z")
        sns = FakeSNS([])

        result = ALERT._evaluate_billing_item(
            item, sns, "arn:aws:sns:us-east-1:000000000000:test-topic", 10,
            max_age_hours=48, now=now,
        )

        self.assertEqual(result["status"], "below_threshold")
        self.assertEqual(result["snapshotAgeSeconds"], 48 * 60 * 60)
        self.assertFalse(sns.paginator_requested)
        self.assertEqual(sns.published, [])

    def test_over_threshold_without_subscribers_does_not_publish(self):
        sns = FakeSNS([])

        result = ALERT._evaluate_billing_item(
            billing_item(), sns, "arn:aws:sns:us-east-1:000000000000:test-topic", 10
        )

        self.assertEqual(result["status"], "sns_no_confirmed_subscribers")
        self.assertFalse(result["published"])
        self.assertEqual(sns.published, [])

    def test_confirmed_subscriber_on_later_page_is_counted(self):
        sns = FakeSNS([], pages=[
            {"Subscriptions": [{"SubscriptionArn": "PendingConfirmation"}]},
            {"Subscriptions": [{"SubscriptionArn": "arn:confirmed-subscription"}]},
        ])

        result = ALERT._evaluate_billing_item(
            billing_item(), sns, "arn:aws:sns:us-east-1:000000000000:test-topic", 10
        )

        self.assertEqual(result["confirmedSubscriptionCount"], 1)
        self.assertEqual(result["pendingSubscriptionCount"], 1)
        self.assertEqual(len(sns.published), 1)

    def test_subscription_lookup_error_does_not_publish(self):
        sns = FakeSNS([], list_error=PermissionError("ListSubscriptionsByTopic denied"))

        with self.assertRaises(PermissionError):
            ALERT._evaluate_billing_item(
                billing_item(), sns, "arn:aws:sns:us-east-1:000000000000:test-topic", 10
            )

        self.assertEqual(sns.published, [])


if __name__ == "__main__":
    unittest.main()
