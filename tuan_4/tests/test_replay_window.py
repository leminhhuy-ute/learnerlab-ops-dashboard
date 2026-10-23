"""The historical SNS replay must not change the product freshness default."""

import importlib.util
from pathlib import Path
import unittest
from datetime import datetime, timedelta, timezone

HELPERS = Path(__file__).parents[2] / "tuan_3" / "tests" / "test_threshold_alert.py"
spec = importlib.util.spec_from_file_location("alert_test_helpers", HELPERS)
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)


class HistoricalReplayWindowTests(unittest.TestCase):
    def test_old_item_is_rejected_by_product_default_and_allowed_only_with_test_window(self):
        now = datetime(2026, 10, 23, 0, 0, tzinfo=timezone.utc)
        item = helpers.billing_item()
        item["collectedAt"] = (now - timedelta(days=10)).isoformat()
        sns = helpers.FakeSNS([{"SubscriptionArn": "arn:confirmed-test-subscription"}])
        normal = helpers.ALERT._evaluate_billing_item(item, sns, "arn:test-topic", 10, now=now)
        self.assertEqual(normal["status"], "stale_billing_snapshot")
        self.assertFalse(normal["published"])
        self.assertEqual(sns.published, [])
        replay = helpers.ALERT._evaluate_billing_item(item, sns, "arn:test-topic", 10, max_age_hours=336, now=now)
        self.assertEqual(replay["status"], "alert_published")
        self.assertTrue(replay["published"])
        self.assertEqual(len(sns.published), 1)


if __name__ == "__main__":
    unittest.main()
