"""Offline safety checks for the week-1 CloudFormation foundation.

Requires PyYAML. This checks project invariants, not AWS permissions or quotas.
AWS CLI validate-template is also run by deploy-week1.ps1 before deployment.
"""

from __future__ import annotations

import argparse
import ipaddress
from pathlib import Path
import sys

try:
    import yaml
except ImportError:
    print("PyYAML is required: python -m pip install PyYAML", file=sys.stderr)
    raise SystemExit(2)


ALLOWED_REGIONS = {"us-east-1", "us-west-2"}
ALLOWED_RESOURCE_TYPES = {
    "AWS::EC2::VPC",
    "AWS::EC2::InternetGateway",
    "AWS::EC2::VPCGatewayAttachment",
    "AWS::EC2::Subnet",
    "AWS::EC2::RouteTable",
    "AWS::EC2::Route",
    "AWS::EC2::SubnetRouteTableAssociation",
    "AWS::S3::Bucket",
}
TAGGABLE_TYPES = {
    "AWS::EC2::VPC", "AWS::EC2::InternetGateway", "AWS::EC2::Subnet",
    "AWS::EC2::RouteTable", "AWS::S3::Bucket",
}


def validate(template: dict) -> list[str]:
    """Return all failures without mutating the template or calling AWS."""
    failures: list[str] = []

    def check(ok: bool, message: str) -> None:
        if not ok:
            failures.append(message)

    check(template.get("AWSTemplateFormatVersion") == "2010-09-09", "Wrong template version")
    parameters = template.get("Parameters", {})
    check("Owner" in parameters and "Default" not in parameters.get("Owner", {}),
          "Owner must be a required parameter")
    check(parameters.get("Project", {}).get("Default") == "learnerlab-ops", "Unexpected Project default")
    check(parameters.get("Environment", {}).get("Default") == "learner-lab"
          and parameters.get("Environment", {}).get("AllowedValues") == ["learner-lab"],
          "Environment must be fixed to learner-lab")
    region_map = template.get("Mappings", {}).get("RegionConfiguration", {})
    check(set(region_map) == ALLOWED_REGIONS, "Only us-east-1 and us-west-2 may appear in the region mapping")
    for region, settings in region_map.items():
        check(settings.get("VpcCidr") == "10.20.0.0/16", f"Unexpected VPC CIDR in {region}")

    resources = template.get("Resources", {})
    check(bool(resources), "Template has no resources")
    for name, resource in resources.items():
        kind = resource.get("Type", "")
        check(kind in ALLOWED_RESOURCE_TYPES, f"Disallowed resource type: {name} ({kind})")
        if kind in TAGGABLE_TYPES:
            tags = {tag.get("Key"): tag.get("Value") for tag in resource.get("Properties", {}).get("Tags", [])}
            check(tags.get("Project") == {"Ref": "Project"}, f"{name}: missing Project tag")
            check(tags.get("Owner") == {"Ref": "Owner"}, f"{name}: missing Owner tag")
            check(tags.get("Environment") == {"Ref": "Environment"}, f"{name}: missing Environment tag")

    vpcs = [resource for resource in resources.values() if resource.get("Type") == "AWS::EC2::VPC"]
    check(len(vpcs) == 1, "Exactly one VPC is required")
    if vpcs:
        check(vpcs[0].get("Properties", {}).get("CidrBlock") == {
            "Fn::FindInMap": ["RegionConfiguration", {"Ref": "AWS::Region"}, "VpcCidr"]
        }, "VPC CIDR must use the allowed-region mapping")

    subnet_networks = []
    subnets = [resource for resource in resources.values() if resource.get("Type") == "AWS::EC2::Subnet"]
    check(len(subnets) == 2, "Exactly two subnets are required")
    for subnet in subnets:
        properties = subnet.get("Properties", {})
        check(properties.get("MapPublicIpOnLaunch") is False, "Automatic public IPv4 assignment must be disabled")
        check(properties.get("VpcId") == {"Ref": "ProjectVpc"}, "Subnet must belong to ProjectVpc")
        try:
            network = ipaddress.ip_network(properties.get("CidrBlock", ""))
            check(network.subnet_of(ipaddress.ip_network("10.20.0.0/16")), "Subnet must be within the VPC")
            subnet_networks.append(network)
        except ValueError:
            failures.append("Invalid subnet CIDR")
    if len(subnet_networks) == 2:
        check(not subnet_networks[0].overlaps(subnet_networks[1]), "Subnet CIDRs overlap")
    az_selectors = [subnet.get("Properties", {}).get("AvailabilityZone") for subnet in subnets]
    check({str(az) for az in az_selectors} == {
        str({"Fn::Select": [0, {"Fn::GetAZs": ""}]}),
        str({"Fn::Select": [1, {"Fn::GetAZs": ""}]}),
    }, "Subnets must select two distinct availability zones")

    route = resources.get("InternetRoute", {})
    check(route.get("DependsOn") == "GatewayAttachment", "Internet route must depend on gateway attachment")
    check(route.get("Properties") == {
        "RouteTableId": {"Ref": "PublicRouteTable"},
        "DestinationCidrBlock": "0.0.0.0/0",
        "GatewayId": {"Ref": "InternetGateway"},
    }, "Unexpected internet route")
    for letter in "AB":
        association = resources.get(f"Subnet{letter}RouteAssociation", {}).get("Properties", {})
        check(association == {
            "SubnetId": {"Ref": f"PublicSubnet{letter}"},
            "RouteTableId": {"Ref": "PublicRouteTable"},
        }, f"Subnet {letter} is not associated with PublicRouteTable")

    buckets = [resource for resource in resources.values() if resource.get("Type") == "AWS::S3::Bucket"]
    check(len(buckets) == 1, "Exactly one artifact bucket is required")
    for bucket in buckets:
        properties = bucket.get("Properties", {})
        check(bucket.get("DeletionPolicy") == "Retain" and bucket.get("UpdateReplacePolicy") == "Retain",
              "S3 bucket must be retained on deletion and replacement")
        check("BucketName" not in properties, "Use a CloudFormation-generated unique bucket name")
        check("WebsiteConfiguration" not in properties, "Week 1 bucket must not publish a website")
        check(properties.get("PublicAccessBlockConfiguration") == {
            "BlockPublicAcls": True, "IgnorePublicAcls": True,
            "BlockPublicPolicy": True, "RestrictPublicBuckets": True,
        }, "All S3 public-access blocks must be enabled")
        check(properties.get("OwnershipControls") == {"Rules": [{"ObjectOwnership": "BucketOwnerEnforced"}]},
              "S3 ACLs must be disabled with BucketOwnerEnforced")
        check(properties.get("BucketEncryption") == {"ServerSideEncryptionConfiguration": [
            {"ServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}
        ]}, "S3 must use SSE-S3 encryption")
        lifecycle = properties.get("LifecycleConfiguration", {}).get("Rules", [])
        check(lifecycle == [{"Id": "AbortIncompleteUploads", "Status": "Enabled",
                             "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 7}}],
              "Lifecycle may only abort incomplete multipart uploads, not delete artifacts")

    output_keys = set(template.get("Outputs", {}))
    check({"AccountId", "Region", "VpcId", "PublicSubnetAId", "PublicSubnetBId",
           "ArtifactBucketName", "LabRoleArn"} <= output_keys, "Missing essential outputs")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("template", nargs="?", type=Path,
                        default=Path(__file__).resolve().parents[1] / "infra" / "week1-foundation.yaml")
    args = parser.parse_args()
    try:
        template = yaml.safe_load(args.template.read_text(encoding="utf-8"))
        if not isinstance(template, dict):
            raise ValueError("Template root must be a mapping")
        failures = validate(template)
    except (OSError, ValueError, yaml.YAMLError, TypeError, AttributeError) as error:
        print(f"FAIL: Cannot validate template: {error}", file=sys.stderr)
        return 1
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print(f"PASS: {args.template}")
    print(f"Checked {len(template['Resources'])} resources: region limits, tags, network, private encrypted retained S3, no compute/IAM.")
    print("Offline checks passed. Check AWS state separately; see docs/week-1/07-deployment-record.md for this Lab.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
