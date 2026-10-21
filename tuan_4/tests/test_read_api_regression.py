"""Regression checks for the Week 2 snapshot reader used by GET /summary.

The fake table exercises the deployed handler's response mapping without AWS
credentials. Live API authorization and DynamoDB comparisons are separate checks.
"""

import importlib.util
import os
import pathlib
import sys
import types
import unittest
from decimal import Decimal
from unittest.mock import patch


SOURCE = pathlib.Path(__file__).parents[2] / "tuan_2" / "src" / "lambdas" / "read-api" / "index.py"
REGIONS = ["us-east-1", "us-west-2"]
SERVICES = ["EC2", "RDS", "SAGEMAKER_ENDPOINT", "SAGEMAKER_NOTEBOOK", "EKS"]


class Expression:
    def __init__(self, clauses):
        self.clauses = clauses

    def __and__(self, other):
        return Expression(self.clauses + other.clauses)


class Key:
    def __init__(self, field):
        self.field = field

    def eq(self, value):
        return Expression([(self.field, "eq", value)])

    def begins_with(self, value):
        return Expression([(self.field, "begins_with", value)])


class FakeTable:
    def __init__(self, items):
        self.items = items
        self.queries = []

    def query(self, **kwargs):
        self.queries.append(kwargs)
        clauses = kwargs["KeyConditionExpression"].clauses
        pk = next(value for field, op, value in clauses if field == "PK" and op == "eq")
        assert ("SK", "begins_with", "SNAPSHOT#") in clauses
        assert kwargs["ScanIndexForward"] is False
        assert kwargs["Limit"] == 1
        matches = sorted(self.items.get(pk, []), key=lambda item: item["SK"], reverse=True)
        return {"Items": matches[:1]}


def load_handler(table):
    boto3 = types.ModuleType("boto3")
    boto3.__path__ = []
    dynamodb = types.ModuleType("boto3.dynamodb")
    dynamodb.__path__ = []
    conditions = types.ModuleType("boto3.dynamodb.conditions")
    conditions.Key = Key
    boto3.resource = lambda service: types.SimpleNamespace(Table=lambda name: table)
    modules = {
        "boto3": boto3,
        "boto3.dynamodb": dynamodb,
        "boto3.dynamodb.conditions": conditions,
    }
    env = {"TABLE": "snapshots", "ACCOUNT": "213858341631", "REGIONS": '["us-east-1","us-west-2"]'}
    spec = importlib.util.spec_from_file_location("week4_read_api", SOURCE)
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, modules), patch.dict(os.environ, env):
        spec.loader.exec_module(module)
    return module


def complete_inventory():
    return {
        f"INVENTORY#{service}#{region}": [
            {
                "SK": "SNAPSHOT#20261021T020000Z",
                "status": "ok",
                "count": 0,
                "collectedAt": "20261021T020000Z",
            }
        ]
        for region in REGIONS
        for service in SERVICES
    }


class ReadApiRegressionTests(unittest.TestCase):
    def test_complete_zero_inventory_and_decimal_billing_remain_distinct(self):
        items = complete_inventory()
        items["BILLING#213858341631"] = [
            {
                "SK": "SNAPSHOT#20261021T020041Z",
                "status": "ok",
                "periodStart": "2026-10-01",
                "periodEndExclusive": "2026-10-22",
                "estimated": True,
                "currency": "USD",
                "total": Decimal("0.0000000001"),
                "serviceTotals": [{"service": "Amazon EC2"}],
                "requestCountToday": 1,
            }
        ]
        table = FakeTable(items)
        response = load_handler(table).handler({}, None)

        self.assertEqual(response["status"], "ok")
        self.assertEqual(len(response["inventory"]), 10)
        self.assertTrue(all(row["status"] == "ok" and row["count"] == 0 for row in response["inventory"]))
        self.assertEqual(Decimal(response["billing"]["total"]), Decimal("0.0000000001"))
        self.assertTrue(response["billing"]["estimated"])
        self.assertEqual(response["billing"]["serviceGroups"], 1)
        self.assertEqual(len(table.queries), 11)

    def test_missing_snapshot_is_not_reported_as_zero_resources(self):
        items = complete_inventory()
        del items["INVENTORY#RDS#us-west-2"]
        table = FakeTable(items)
        response = load_handler(table).handler({}, None)

        self.assertEqual(response["status"], "partial")
        missing = next(row for row in response["inventory"] if row["service"] == "RDS" and row["region"] == "us-west-2")
        self.assertEqual(missing["status"], "missing")
        self.assertIsNone(missing["count"])
        self.assertEqual(response["billing"]["status"], "missing")

    def test_newest_snapshot_is_selected(self):
        items = complete_inventory()
        items["INVENTORY#EC2#us-east-1"].append(
            {"SK": "SNAPSHOT#20261022T020000Z", "status": "unavailable", "count": None, "errorCode": "AccessDenied"}
        )
        response = load_handler(FakeTable(items)).handler({}, None)

        ec2 = next(row for row in response["inventory"] if row["service"] == "EC2" and row["region"] == "us-east-1")
        self.assertEqual(response["status"], "partial")
        self.assertEqual(ec2["status"], "unavailable")
        self.assertIsNone(ec2["count"])
        self.assertEqual(ec2["errorCode"], "AccessDenied")


if __name__ == "__main__":
    unittest.main()
