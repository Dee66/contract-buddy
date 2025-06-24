"""
Automates the conversion of environment YAML config to JSON and uploads it to AWS SSM Parameter Store.
This ensures your SSM config is always in sync with your versioned YAML, supporting reproducible, AWS-native deployments.

Usage:
    python scripts/config_to_ssm.py --env dev
    python scripts/config_to_ssm.py --env staging
    python scripts/config_to_ssm.py --env prod

Requires:
    - boto3 (`pip install boto3 pyyaml types-PyYAML`)
    - AWS credentials and region configured (via env vars or `aws configure`)
"""

import argparse
import os
import sys
import json
import yaml  # mypy requires types-PyYAML for type checking
import boto3
from botocore.exceptions import ClientError

# NOTE: mypy [import-untyped] errors for "yaml" mean types-PyYAML is missing in the environment where mypy runs.
# To resolve for all environments (dev, staging, prod):
#   pip install types-PyYAML
# If using pre-commit, also run:
#   pre-commit clean && pre-commit install


def load_yaml_config(env: str) -> dict:
    config_path = os.path.join("config", f"{env}.yaml")
    if not os.path.exists(config_path):
        print(f"ERROR: {config_path} does not exist.")
        sys.exit(1)
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def upload_to_ssm(param_name: str, value: dict, region: str):
    ssm = boto3.client("ssm", region_name=region)
    try:
        ssm.put_parameter(
            Name=param_name,
            Value=json.dumps(value),
            Type="String",
            Overwrite=True,
        )
        print(f"Uploaded config to SSM: {param_name} in {region}")
    except ClientError as e:
        print(f"ERROR: Failed to upload to SSM: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Push environment config to AWS SSM Parameter Store"
    )
    parser.add_argument(
        "--env",
        required=True,
        choices=["dev", "staging", "prod"],
        help="Target environment",
    )
    parser.add_argument(
        "--region",
        default=os.environ.get("AWS_REGION", "af-south-1"),
        help="AWS region",
    )
    args = parser.parse_args()

    param_name = f"/codecraft-ai/{args.env}/AppConfig"
    config = load_yaml_config(args.env)
    upload_to_ssm(param_name, config, args.region)


if __name__ == "__main__":
    main()
