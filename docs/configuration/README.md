# Configuration & Secrets Validation Workflow

This project enforces **pre-deployment validation** of all AWS SSM Parameter Store config and AWS Secrets Manager secrets using the actual Pydantic schemas from the codebase.

## Why

- Prevents runtime failures due to missing or malformed config/secrets.
- Ensures all environments are validated before deployment.
- Detects drift between code, infrastructure, and documentation.
- Demonstrates operational maturity and AWS Well-Architected best practices.
- **Automates doc/schema generation:** The config schema doc is generated from the Pydantic model to guarantee alignment.
- **Observability:** Config version and validation status are emitted as metrics/logs for operational dashboards.

## How

- Run locally:
  `make validate-config CDK_ENV=dev`
  or
  `python scripts/validate_config.py --env all`
- Run in CI/CD:
  See `.github/workflows/validate-config.yml` for automated validation on every PR and deploy.
- Regenerate config schema doc:
  `python scripts/generate_config_schema_md.py`

## Features

- **Single source of truth:** Uses Pydantic models for validation.
- **Multi-environment:** Validates all environments in one run.
- **Drift detection:** Surfaces missing/extra keys vs. code schema, CDK, and docs.
- **Automated doc generation:** Keeps config schema doc in sync with code.
- **Robust error handling:** Fails fast on AWS auth/config issues.
- **CI-friendly output:** Colorized, tabular summary for reviewers.
- **Unit tested:** Validator logic is covered by automated tests.
- **Observability:** Config version and validation status are emitted as metrics/logs.

## Extending

- Update the Pydantic models to add/remove config or secret keys.
- The validator and docs will automatically detect and report drift.
- Add new tests in `tests/scripts/test_validate_config.py` to ensure validator robustness.
