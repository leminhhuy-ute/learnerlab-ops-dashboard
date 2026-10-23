"""One bounded billing collection and a live inventory/API regression pass."""

import datetime as dt
from decimal import Decimal
import json
from pathlib import Path
import urllib.error
import urllib.request

import boto3
from boto3.dynamodb.conditions import Key
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

ACCOUNT = "213858341631"
REGION = "us-east-1"
OUT = Path.home() / "week4-final-20261023"
URL = "https://qvpnt8h5yh.execute-api.us-east-1.amazonaws.com/summary"


if __name__ == "__main__":
    assert boto3.client("sts", region_name=REGION).get_caller_identity()["Account"] == ACCOUNT
    assert not (OUT / "final-live-flow.json").exists(), "Inspect existing evidence before calling billing again"
    assert not (OUT / "billing-collection-receipt.json").exists(), "Billing already called: resume read-only checks instead"
    table = boto3.resource("dynamodb", region_name=REGION).Table("learnerlab-ops-week2-snapshots")
    lam = boto3.client("lambda", region_name=REGION)
    def invoke(name):
        response = lam.invoke(FunctionName=name, Payload=b"{}")
        data = json.loads(response["Payload"].read())
        assert response["StatusCode"] == 200 and not response.get("FunctionError"), data.get("errorType")
        return data
    inventory = invoke("learnerlab-ops-week2-inventory-core")
    assert len(inventory["results"]) == 10 and all(r["status"] == "ok" for r in inventory["results"])
    date = dt.datetime.now(dt.timezone.utc).date().isoformat()
    budget = table.get_item(Key={"PK": f"CE#{ACCOUNT}#{date}", "SK": "BUDGET"}, ConsistentRead=True).get("Item", {})
    attempts = int(budget.get("attempts", 0))
    assert attempts < 4, "Daily Cost Explorer attempt budget exhausted"
    bill = invoke("learnerlab-ops-week2-billing-collector")
    assert bill["status"] == "ok" and int(bill["requestCountToday"]) <= 4
    (OUT / "billing-collection-receipt.json").write_text(json.dumps({k: bill[k] for k in ("status", "snapshotId", "requestCountToday", "estimated", "periodStart", "periodEndExclusive")}, indent=2))
    alert = invoke("learnerlab-ops-week2-threshold-alert")
    assert alert["status"] == "below_threshold" and not alert["published"]
    assert alert["thresholdUsd"] == "10" and alert["maxSnapshotAgeHours"] == 48
    request = AWSRequest(method="GET", url=URL)
    SigV4Auth(boto3.Session().get_credentials().get_frozen_credentials(), "execute-api", REGION).add_auth(request)
    response = urllib.request.urlopen(urllib.request.Request(URL, headers=dict(request.headers)))
    api = json.load(response)
    try:
        unsigned = urllib.request.urlopen(URL).status
    except urllib.error.HTTPError as exc:
        unsigned = exc.code
    matches = 0
    for row in api["inventory"]:
        item = table.query(KeyConditionExpression=Key("PK").eq(f"INVENTORY#{row['service']}#{row['region']}") & Key("SK").begins_with("SNAPSHOT#"), ScanIndexForward=False, Limit=1, ConsistentRead=True)["Items"][0]
        matches += all(row[k] == item.get(k) for k in ("status", "count", "collectedAt"))
    latest_bill = table.query(KeyConditionExpression=Key("PK").eq("BILLING#" + ACCOUNT) & Key("SK").begins_with("SNAPSHOT#"), ScanIndexForward=False, Limit=1, ConsistentRead=True)["Items"][0]
    billing_match = Decimal(str(api["billing"]["total"])) == latest_bill["total"] and all(api["billing"].get(k) == latest_bill.get(k) for k in ("status", "periodStart", "periodEndExclusive", "estimated", "currency"))
    assert matches == 10 and billing_match and api["status"] == "ok" and response.status == 200 and unsigned == 403
    result = {"checkedAtUtc": dt.datetime.now(dt.timezone.utc).isoformat(), "inventory": inventory,
        "billing": {k: bill[k] for k in ("status", "snapshotId", "periodStart", "periodEndExclusive", "estimated", "requestCountToday")},
        "billingCollectorInvocationsThisRun": 1, "ceBudgetAttemptsBefore": attempts,
        "productAlert": {k: alert[k] for k in ("status", "published", "snapshotId", "collectedAt", "snapshotAgeSeconds", "maxSnapshotAgeHours", "thresholdUsd")},
        "api": {"signedHttp": response.status, "unsignedHttp": unsigned, "status": api["status"], "inventorySnapshotMatches": matches, "billingSnapshotMatches": billing_match}}
    (OUT / "final-live-flow.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result))
