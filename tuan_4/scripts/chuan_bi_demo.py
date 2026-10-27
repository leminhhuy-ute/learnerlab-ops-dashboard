"""Read-only preparation for the Learner Lab demonstration.

Run in AWS CloudShell. Reads the existing authenticated API and a billing
timestamp. Writes private local files only; does not invoke collectors,
change AWS resources, call Cost Explorer, or publish SNS messages.
"""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import urllib.error
import urllib.request

import boto3
from boto3.dynamodb.conditions import Key
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from botocore.exceptions import BotoCoreError, ClientError


ACCOUNT = "213858341631"
REGION = "us-east-1"
API = "https://qvpnt8h5yh.execute-api.us-east-1.amazonaws.com/summary"
TABLE = "learnerlab-ops-week2-snapshots"
BUCKET = "learnerlab-ops-week2-dashboard-213858341631"


def get_http(headers=None):
    request = urllib.request.Request(API, headers=headers or {})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as error:
        return error.code, b""


def private_file(path, content):
    path.write_text(content, encoding="utf-8")
    path.chmod(0o600)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview", action="store_true", help="Save a private S3 preview URL, valid for at most 15 minutes")
    args = parser.parse_args()

    session = boto3.Session(region_name=REGION)
    identity = session.client("sts").get_caller_identity()
    if identity["Account"] != ACCOUNT:
        raise RuntimeError("Wrong AWS account. Stop and open the correct Learner Lab.")

    credentials = session.get_credentials()
    if credentials is None:
        raise RuntimeError("No active AWS credentials. Restart the Learner Lab session.")

    unsigned_http, _ = get_http()
    request = AWSRequest(method="GET", url=API)
    SigV4Auth(credentials.get_frozen_credentials(), "execute-api", REGION).add_auth(request)
    signed_http, body = get_http(dict(request.headers))
    print("Checked UTC:", datetime.now(timezone.utc).isoformat(timespec="seconds"))
    print("AWS account:", ACCOUNT, "| Region:", REGION)
    print("GET /summary without signature:", unsigned_http)
    print("GET /summary with SigV4:", signed_http)
    if unsigned_http != 403 or signed_http != 200:
        raise RuntimeError("Unexpected API result. Check the session and AWS_IAM configuration before recording.")

    payload = json.loads(body)
    if "body" in payload:
        payload = json.loads(payload["body"]) if isinstance(payload["body"], str) else payload["body"]
    if not isinstance(payload.get("inventory"), list) or not isinstance(payload.get("billing"), dict):
        raise RuntimeError("API response does not have the expected inventory/billing structure.")

    output = Path.home() / "demo-24110019"
    output.mkdir(mode=0o700, parents=True, exist_ok=True)
    private_file(output / "summary.json", json.dumps(payload, ensure_ascii=False, indent=2))
    inventory = payload["inventory"]
    billing = payload["billing"]
    print("API status:", payload.get("status"))
    print("Inventory rows:", len(inventory))
    print("Inventory ok rows:", sum(row.get("status") == "ok" for row in inventory))
    print("Inventory collectedAt:", ", ".join(sorted({str(row.get("collectedAt")) for row in inventory})))
    print("Billing status:", billing.get("status"), "| estimated:", billing.get("estimated"))
    print("Billing period:", billing.get("periodStart"), "to before", billing.get("periodEndExclusive"))

    try:
        result = session.resource("dynamodb").Table(TABLE).query(
            KeyConditionExpression=Key("PK").eq("BILLING#" + ACCOUNT),
            ScanIndexForward=False,
            Limit=1,
        )
        items = result.get("Items") or []
        print("Billing collectedAt:", items[0].get("collectedAt") if items else "missing")
    except ClientError as error:
        print("Billing timestamp query:", error.response["Error"]["Code"])

    print("Private API JSON:", output / "summary.json")
    if args.preview:
        url = session.client("s3").generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET, "Key": "index.html", "ResponseContentDisposition": "inline"},
            ExpiresIn=900,
        )
        private_file(output / "dashboard-url-private.txt", url)
        print("Private preview URL saved to:", output / "dashboard-url-private.txt")
        print("Open that file BEFORE recording. Do not show the signed URL in the video.")
    print("No AWS resources changed. No Cost Explorer request or SNS Publish was made.")


if __name__ == "__main__":
    try:
        main()
    except ClientError as error:
        print("AWS error:", error.response["Error"]["Code"], file=sys.stderr)
        sys.exit(1)
    except (BotoCoreError, RuntimeError, ValueError, OSError) as error:
        print("Preparation stopped:", str(error), file=sys.stderr)
        sys.exit(1)
