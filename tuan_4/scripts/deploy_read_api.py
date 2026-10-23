"""Deploy the tested snapshot reader, then exercise a disposable empty table.

Run in CloudShell with the current Lab session. Backs up product code before
updating it with RevisionId, verifies source/code hashes and preserves config.
Temporary test resources have fixed names/tags and are removed after evidence.
"""

import argparse
import base64
import datetime as dt
from decimal import Decimal
import hashlib
import io
import json
from pathlib import Path
import urllib.error
import urllib.request
import zipfile

import boto3
from boto3.dynamodb.conditions import Key
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from botocore.exceptions import ClientError

ACCOUNT = "213858341631"
REGION = "us-east-1"
FUNCTION = "learnerlab-ops-week2-read-api"
TEST = "learnerlab-ops-week4-empty-snapshot-test"
TABLE = "learnerlab-ops-week2-snapshots"
URL = "https://qvpnt8h5yh.execute-api.us-east-1.amazonaws.com/summary"
OUT = Path.home() / "week4-final-20261023"
TAGS = {"Project": "learnerlab-ops", "Owner": "24110019", "Purpose": "week4-disposable-empty-test"}


def save(name, value):
    value = {"checkedAtUtc": dt.datetime.now(dt.timezone.utc).isoformat(), **value}
    (OUT / name).write_text(json.dumps(value, indent=2), encoding="utf-8")
    print(json.dumps(value))


def absent(call, **kwargs):
    try:
        call(**kwargs)
        return False
    except ClientError as exc:
        if exc.response["Error"]["Code"] in {"ResourceNotFoundException", "ResourceNotFound"}:
            return True
        raise


def config_fields(config):
    return {k: config.get(k) for k in ("Handler", "Runtime", "Role", "Timeout", "MemorySize", "Architectures", "Environment")}


def payload(lam, name):
    response = lam.invoke(FunctionName=name, Payload=b"{}")
    body = json.loads(response["Payload"].read())
    assert response["StatusCode"] == 200 and not response.get("FunctionError"), body.get("errorType")
    return body


def main(source):
    assert boto3.client("sts", region_name=REGION).get_caller_identity()["Account"] == ACCOUNT
    OUT.mkdir(exist_ok=True)
    lam = boto3.client("lambda", region_name=REGION)
    ddb = boto3.client("dynamodb", region_name=REGION)
    logs = boto3.client("logs", region_name=REGION)
    function = lam.get_function(FunctionName=FUNCTION)
    before = function["Configuration"]
    assert before["Handler"] == "index.handler" and before["Role"].endswith(":role/LabRole")
    assert before["Environment"]["Variables"]["TABLE"] == TABLE
    old_zip = urllib.request.urlopen(function["Code"]["Location"]).read()
    backup = OUT / "read-api-before.zip"
    if backup.exists():
        raise RuntimeError("A deployment backup already exists; inspect it before rerunning")
    backup.write_bytes(old_zip)
    (OUT / "read-api-before-config.json").write_text(json.dumps(config_fields(before), indent=2))
    code = source.read_bytes()
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("index.py", code)
    package = archive.getvalue()
    updated = lam.update_function_code(FunctionName=FUNCTION, ZipFile=package, RevisionId=before["RevisionId"])
    lam.get_waiter("function_updated_v2").wait(FunctionName=FUNCTION)
    after = lam.get_function(FunctionName=FUNCTION)
    deployed = urllib.request.urlopen(after["Code"]["Location"]).read()
    assert zipfile.ZipFile(io.BytesIO(deployed)).read("index.py") == code
    assert after["Configuration"]["CodeSha256"] == base64.b64encode(hashlib.sha256(package).digest()).decode()
    assert config_fields(after["Configuration"]) == config_fields(before)
    normal = payload(lam, FUNCTION)
    save("reader-deployment.json", {"function": FUNCTION, "lastUpdateStatus": after["Configuration"]["LastUpdateStatus"],
         "sourceSha256": hashlib.sha256(code).hexdigest(), "codeSha256Base64": updated["CodeSha256"],
         "backupZipSha256": hashlib.sha256(old_zip).hexdigest(), "configurationUnchanged": True,
         "productStatus": normal["status"], "inventoryRows": len(normal["inventory"]), "billingStatus": normal["billing"]["status"]})

    assert absent(lam.get_function, FunctionName=TEST), "Test function name already exists"
    assert absent(ddb.describe_table, TableName=TEST), "Test table name already exists"
    group = "/aws/lambda/" + TEST
    assert not [g for g in logs.describe_log_groups(logGroupNamePrefix=group)["logGroups"] if g["logGroupName"] == group]
    created_table = created_function = False
    try:
        ddb.create_table(TableName=TEST, BillingMode="PAY_PER_REQUEST",
            KeySchema=[{"AttributeName": "PK", "KeyType": "HASH"}, {"AttributeName": "SK", "KeyType": "RANGE"}],
            AttributeDefinitions=[{"AttributeName": "PK", "AttributeType": "S"}, {"AttributeName": "SK", "AttributeType": "S"}],
            Tags=[{"Key": k, "Value": v} for k, v in TAGS.items()])
        created_table = True
        ddb.get_waiter("table_exists").wait(TableName=TEST)
        env = {**before["Environment"]["Variables"], "TABLE": TEST}
        lam.create_function(FunctionName=TEST, Runtime=before["Runtime"], Role=before["Role"], Handler="index.handler",
            Code={"ZipFile": package}, Timeout=30, MemorySize=128, Environment={"Variables": env}, Tags=TAGS)
        created_function = True
        lam.get_waiter("function_active_v2").wait(FunctionName=TEST)
        empty = payload(lam, TEST)
        assert empty["status"] == "partial" and len(empty["inventory"]) == 10
        assert all(x["status"] == "missing" and x["count"] is None for x in empty["inventory"])
        assert empty["billing"]["status"] == "missing"
        save("reader-empty-table.json", {"isolatedTable": TEST, "sourceSha256": hashlib.sha256(code).hexdigest(),
             "lambdaStatusCode": 200, "functionError": None, "status": empty["status"],
             "missingInventoryRows": len(empty["inventory"]), "allMissingCountsNull": True,
             "billingStatus": empty["billing"]["status"], "productTableUnmodified": True, "response": empty})
    finally:
        if created_function:
            lam.delete_function(FunctionName=TEST)
        if created_table:
            ddb.delete_table(TableName=TEST)
            ddb.get_waiter("table_not_exists").wait(TableName=TEST)
        if created_function and not absent(logs.describe_log_streams, logGroupName=group, limit=1):
            logs.delete_log_group(logGroupName=group)
        save("reader-test-cleanup.json", {"testFunctionAbsent": absent(lam.get_function, FunctionName=TEST),
             "testTableAbsent": absent(ddb.describe_table, TableName=TEST),
             "testLogGroupAbsent": absent(logs.describe_log_streams, logGroupName=group, limit=1)})

    unsigned = None
    try:
        unsigned = urllib.request.urlopen(URL).status
    except urllib.error.HTTPError as exc:
        unsigned = exc.code
    request = AWSRequest(method="GET", url=URL)
    SigV4Auth(boto3.Session().get_credentials().get_frozen_credentials(), "execute-api", REGION).add_auth(request)
    response = urllib.request.urlopen(urllib.request.Request(URL, headers=dict(request.headers)))
    api = json.load(response)
    table = boto3.resource("dynamodb", region_name=REGION).Table(TABLE)
    def latest(pk):
        return table.query(KeyConditionExpression=Key("PK").eq(pk) & Key("SK").begins_with("SNAPSHOT#"), ScanIndexForward=False, Limit=1)["Items"][0]
    matches = 0
    for row in api["inventory"]:
        snapshot = latest(f"INVENTORY#{row['service']}#{row['region']}")
        matches += all(row[k] == snapshot.get(k) for k in ("status", "count", "collectedAt"))
    bill = latest("BILLING#" + ACCOUNT)
    bill_match = all(api["billing"].get(k) == bill.get(k) for k in ("status", "periodStart", "periodEndExclusive", "estimated", "currency")) and Decimal(str(api["billing"]["total"])) == Decimal(str(bill["total"]))
    assert response.status == 200 and unsigned == 403 and matches == 10 and bill_match
    save("reader-api-regression.json", {"unsignedHttp": unsigned, "signedHttp": response.status, "status": api["status"],
         "inventorySnapshotMatches": matches, "inventoryRows": len(api["inventory"]), "billingSnapshotMatches": bill_match,
         "billingCollectedAt": bill["collectedAt"], "estimated": bool(bill.get("estimated", True)),
         "periodStart": bill.get("periodStart"), "periodEndExclusive": bill.get("periodEndExclusive")})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("/tmp/week4-read-api-index.py"))
    main(parser.parse_args().source)
