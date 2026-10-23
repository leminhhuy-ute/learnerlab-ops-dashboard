"""Back up and update the private S3 dashboard; keep preview/API data local."""

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import urllib.request

import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

ACCOUNT = "213858341631"
REGION = "us-east-1"
BUCKET = "learnerlab-ops-week2-dashboard-213858341631"
URL = "https://qvpnt8h5yh.execute-api.us-east-1.amazonaws.com/summary"
OUT = Path.home() / "week4-final-20261023"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("/tmp/week4-dashboard.html"))
    args = parser.parse_args()
    assert boto3.client("sts", region_name=REGION).get_caller_identity()["Account"] == ACCOUNT
    OUT.mkdir(exist_ok=True)
    s3 = boto3.client("s3", region_name=REGION)
    before = s3.get_object(Bucket=BUCKET, Key="index.html")
    (OUT / "dashboard-before.html").write_bytes(before["Body"].read())
    bpa = s3.get_public_access_block(Bucket=BUCKET)["PublicAccessBlockConfiguration"]
    assert all(bpa.values())
    source = args.source.read_bytes()
    response = s3.put_object(Bucket=BUCKET, Key="index.html", Body=source,
        ContentType="text/html; charset=utf-8", ServerSideEncryption="AES256")
    current = s3.get_object(Bucket=BUCKET, Key="index.html")
    assert current["Body"].read() == source
    assert s3.get_public_access_block(Bucket=BUCKET)["PublicAccessBlockConfiguration"] == bpa
    result = {"checkedAtUtc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "bucket": BUCKET, "sourceSha256": hashlib.sha256(source).hexdigest(),
        "putHttpStatus": response["ResponseMetadata"]["HTTPStatusCode"], "objectMatchesRepo": True,
        "publicAccessBlockUnchanged": True, "encryption": current.get("ServerSideEncryption")}
    (OUT / "dashboard-deployment.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result))
    # The preview URL and raw billing payload are private local artifacts only.
    preview = s3.generate_presigned_url("get_object", Params={"Bucket": BUCKET, "Key": "index.html"}, ExpiresIn=900)
    (OUT / "dashboard-preview-url.txt").write_text(preview)
    request = AWSRequest(method="GET", url=URL)
    SigV4Auth(boto3.Session().get_credentials().get_frozen_credentials(), "execute-api", REGION).add_auth(request)
    api = json.load(urllib.request.urlopen(urllib.request.Request(URL, headers=dict(request.headers))))
    (OUT / "api-summary-private.json").write_text(json.dumps(api))
