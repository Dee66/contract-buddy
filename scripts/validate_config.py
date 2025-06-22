# scripts/validate_config.py
"""
Validates AWS SSM Parameter Store config and (optionally) AWS Secrets Manager secrets
against the project's Pydantic schema(s) before deployment.

- Fails fast and prints actionable errors if config is missing or invalid.
- Can be run locally or in CI/CD (uses default AWS credentials).
- Designed for extensibility and portfolio-grade clarity.
"""

import argparse
import boto3
import json
import os
import sys
from typing import List, Dict, Set

try:
    from termcolor import colored
except ImportError:

    def colored(text, color=None, attrs=None):
        return text  # fallback if termcolor not installed


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.adapters.config_manager import AppConfig

from pydantic import BaseModel, ValidationError


# --- Pydantic schema for secrets validation ---
class AppSecrets(BaseModel):
    DB_HOST: str
    DB_PORT: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str
    S3_BUCKET_NAME: str
    S3_REGION: str
    API_KEY: str
    API_ENDPOINT: str
    LOG_LEVEL: str
    MONITORING_ENDPOINT: str
    ENCRYPTION_KEY: str
    JWT_SECRET: str
    MODEL_REGISTRY_URL: str
    MODEL_VERSION: str
    COST_TRACKING_ID: str
    TRACING_ENDPOINT: str


def fetch_ssm_json_param(ssm, param_name: str) -> dict:
    try:
        resp = ssm.get_parameter(Name=param_name, WithDecryption=True)
        return json.loads(resp["Parameter"]["Value"])
    except Exception as e:
        print(
            colored(
                f"[ERROR] Failed to fetch or parse SSM parameter '{param_name}': {e}",
                "red",
            )
        )
        return None


def fetch_secret_json(secrets, secret_name: str) -> dict:
    try:
        resp = secrets.get_secret_value(SecretId=secret_name)
        return json.loads(resp["SecretString"])
    except Exception as e:
        print(
            colored(
                f"[ERROR] Failed to fetch or parse secret '{secret_name}': {e}", "red"
            )
        )
        return None


def validate_app_config(ssm, env: str) -> (bool, Set[str]):
    param_name = f"/codecraft-ai/{env}/AppConfig"
    config_dict = fetch_ssm_json_param(ssm, param_name)
    if not config_dict:
        print(colored(f"[FAIL] {param_name} missing or unreadable.", "red"))
        return False, set()
    try:
        AppConfig(**config_dict)
        print(colored(f"[OK] {param_name} is valid.", "green"))
        return True, set(config_dict.keys())
    except ValidationError as e:
        print(colored(f"[FAIL] {param_name} is INVALID: {e}", "red"))
        return False, set(config_dict.keys())


def validate_app_secrets(secrets, env: str) -> (bool, Set[str]):
    secret_name = f"codecraft-ai/secrets/{env}"
    secret_dict = fetch_secret_json(secrets, secret_name)
    if not secret_dict:
        print(colored(f"[FAIL] {secret_name} missing or unreadable.", "red"))
        return False, set()
    try:
        AppSecrets(**secret_dict)
        print(colored(f"[OK] {secret_name} is valid.", "green"))
        return True, set(secret_dict.keys())
    except ValidationError as e:
        print(colored(f"[FAIL] {secret_name} is INVALID: {e}", "red"))
        return False, set(secret_dict.keys())


def print_summary(results: List[Dict]):
    print("\nValidation Summary:")
    print("-" * 60)
    print(
        "{:<12} {:<18} {:<10} {:<20}".format(
            "Environment", "Config Type", "Status", "Details"
        )
    )
    print("-" * 60)
    for r in results:
        status = (
            colored("PASS", "green")
            if r["ok"]
            else colored("FAIL", "red", attrs=["bold"])
        )
        print(
            "{:<12} {:<18} {:<10} {:<20}".format(
                r["env"], r["type"], status, r["details"]
            )
        )
    print("-" * 60)
    if all(r["ok"] for r in results):
        print(
            colored(
                "[SUCCESS] All config and secrets validated successfully.",
                "green",
                attrs=["bold"],
            )
        )
    else:
        print(
            colored(
                "[ERROR] One or more validations failed. Deployment should be blocked.",
                "red",
                attrs=["bold"],
            )
        )


def discover_environments(ssm) -> List[str]:
    """Dynamically discover all environments by listing SSM parameters under /codecraft-ai/."""
    try:
        envs = set()
        paginator = ssm.get_paginator("describe_parameters")
        for page in paginator.paginate(
            ParameterFilters=[
                {"Key": "Name", "Option": "BeginsWith", "Values": ["/codecraft-ai/"]}
            ]
        ):
            for param in page["Parameters"]:
                parts = param["Name"].split("/")
                if len(parts) >= 4 and parts[2] not in envs:
                    envs.add(parts[2])
        return sorted(envs)
    except Exception as e:
        print(colored(f"[ERROR] Failed to discover environments from SSM: {e}", "red"))
        return ["dev", "staging", "prod"]


def get_environments(arg_env: str, ssm) -> List[str]:
    if arg_env.lower() == "all":
        return discover_environments(ssm)
    return [arg_env]


def check_drift(
    actual_keys: Set[str],
    expected_keys: Set[str],
    label: str,
    env: str,
    results: List[Dict],
):
    missing = expected_keys - actual_keys
    extra = actual_keys - expected_keys
    if missing or extra:
        drift_msg = ""
        if missing:
            drift_msg += f"Missing: {sorted(missing)} "
        if extra:
            drift_msg += f"Extra: {sorted(extra)}"
        results.append(
            {"env": env, "type": f"{label} Drift", "ok": False, "details": drift_msg}
        )
        print(
            colored(
                f"[DRIFT] {label} keys drift detected for {env}: {drift_msg}", "yellow"
            )
        )
    else:
        results.append(
            {"env": env, "type": f"{label} Drift", "ok": True, "details": "No drift"}
        )


def parse_cdk_config_keys(cdk_json_path: str) -> Set[str]:
    """
    Parse the CDK-generated config schema (JSON or synthesized output) for config keys.
    This is a stub: adapt to your actual CDK output format.
    """
    try:
        with open(cdk_json_path, "r") as f:
            cdk_config = json.load(f)
        # Example: extract keys from a known structure
        # Adjust this logic to match your CDK output
        return set(cdk_config.get("AppConfig", {}).keys())
    except Exception as e:
        print(colored(f"[WARN] Could not parse CDK config keys: {e}", "yellow"))
        return set()


def parse_docs_config_keys(docs_md_path: str) -> Set[str]:
    """
    Parse the Markdown config schema doc for config keys.
    This is a stub: adapt to your actual doc format.
    """
    try:
        keys = set()
        with open(docs_md_path, "r") as f:
            for line in f:
                if line.strip().startswith("- "):
                    key = line.split("**")[1] if "**" in line else None
                    if key:
                        keys.add(key.strip())
        return keys
    except Exception as e:
        print(colored(f"[WARN] Could not parse docs config keys: {e}", "yellow"))
        return set()


def main():
    parser = argparse.ArgumentParser(
        description="Validate SSM config and secrets before deployment."
    )
    parser.add_argument(
        "--env",
        required=True,
        help="Environment name (e.g., dev, staging, prod, or 'all')",
    )
    parser.add_argument(
        "--region", default=os.environ.get("AWS_REGION", "us-east-1"), help="AWS region"
    )
    args = parser.parse_args()

    try:
        ssm = boto3.client("ssm", region_name=args.region)
        secrets = boto3.client("secretsmanager", region_name=args.region)
        # Test AWS credentials early
        ssm.describe_parameters(MaxResults=1)
    except Exception as e:
        print(
            colored(
                f"[FATAL] AWS credentials/configuration error: {e}",
                "red",
                attrs=["bold"],
            )
        )
        sys.exit(3)

    results = []
    # Expected keys for drift detection
    expected_config_keys = set(AppConfig.schema()["properties"].keys())
    expected_secret_keys = set(AppSecrets.schema()["properties"].keys())

    for env in get_environments(args.env, ssm):
        ok_config, config_keys = validate_app_config(ssm, env)
        results.append(
            {
                "env": env,
                "type": "SSM Config",
                "ok": ok_config,
                "details": "" if ok_config else "Invalid or missing",
            }
        )
        ok_secrets, secret_keys = validate_app_secrets(secrets, env)
        results.append(
            {
                "env": env,
                "type": "Secrets",
                "ok": ok_secrets,
                "details": "" if ok_secrets else "Invalid or missing",
            }
        )

        # --- Schema/Infra/Docs Drift Detection ---
        check_drift(config_keys, expected_config_keys, "Config", env, results)
        check_drift(secret_keys, expected_secret_keys, "Secrets", env, results)

    # --- Automated Drift Check Against Docs/CDK ---
    cdk_keys = parse_cdk_config_keys("infrastructure/cdk_config_schema.json")
    docs_keys = parse_docs_config_keys("docs/configuration/config_schema.md")
    expected_config_keys = set(AppConfig.schema()["properties"].keys())

    if cdk_keys:
        check_drift(cdk_keys, expected_config_keys, "CDK vs Code", "all", results)
    if docs_keys:
        check_drift(docs_keys, expected_config_keys, "Docs vs Code", "all", results)

    print_summary(results)
    if not all(r["ok"] for r in results):
        sys.exit(2)


if __name__ == "__main__":
    main()
