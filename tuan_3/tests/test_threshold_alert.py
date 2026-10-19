import importlib.util
import pathlib
import unittest


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
    def __init__(self, subscriptions):
        self.subscriptions = subscriptions
        self.published = []
        self.paginator_requested = False

    def get_paginator(self, operation):
        if operation != "list_subscriptions_by_topic":
            raise AssertionError(f"Unexpected paginator: {operation}")
        self.paginator_requested = True
        return FakePaginator([{"Subscriptions": self.subscriptions}])

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

    def test_over_threshold_without_subscribers_does_not_publish(self):
        sns = FakeSNS([])

        result = ALERT._evaluate_billing_item(
            billing_item(), sns, "arn:aws:sns:us-east-1:000000000000:test-topic", 10
        )

        self.assertEqual(result["status"], "sns_no_confirmed_subscribers")
        self.assertFalse(result["published"])
        self.assertEqual(sns.published, [])


if __name__ == "__main__":
    unittest.main()
