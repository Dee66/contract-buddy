from pathlib import Path
import nox
from utils import ensure_bootstrap, get_env

# 🟪 ARCH: Do NOT import from cdk.py within itself. Remove any `from cdk import ...` lines to prevent circular imports.
# 🟦 NOTE: All session functions are registered via the @nox.session decorator and discovered by Nox automatically.


@nox.session
def cdk_diff(session):
    """
    Detect infrastructure drift using AWS CDK.
    🟨 CAUTION: Fails fast if CDK or dependencies are not installed or if the stack is misconfigured.
    🟦 NOTE: Ensures poetry environment and CDK CLI are available before running.
    """
    ensure_bootstrap(session)
    app_path = Path("infrastructure/app.py")
    if not app_path.exists():
        session.skip(
            "🟨 CAUTION: infrastructure/app.py not found. Skipping CDK diff step."
        )
        return
    try:
        session.run(
            "poetry",
            "run",
            "cdk",
            "--version",
            external=True,
            silent=True,
        )
    except Exception:
        session.error(
            "🟥 CRITICAL: AWS CDK CLI is not installed in the poetry environment. Run 'poetry run pip install aws-cdk-lib awscli'."
        )

    try:
        session.run(
            "poetry",
            "run",
            "cdk",
            "-a",
            "python infrastructure/app.py",
            "diff",
            external=True,
        )
    except Exception as e:
        session.error(f"🟥 CRITICAL: CDK diff failed: {e}")


@nox.session
def cdk_deploy(session):
    """Deploy infrastructure using AWS CDK for the selected environment."""
    ensure_bootstrap(session)
    env = get_env(session)
    app_path = Path("infrastructure/app.py")
    if not app_path.exists():
        session.skip(
            "🟨 CAUTION: infrastructure/app.py not found. Skipping CDK deploy step."
        )
        return
    try:
        session.run(
            "poetry",
            "run",
            "cdk",
            "--version",
            external=True,
            silent=True,
        )
    except Exception:
        session.error(
            "🟥 CRITICAL: AWS CDK CLI is not installed in the poetry environment. Run 'poetry run pip install aws-cdk-lib awscli'."
        )

    try:
        session.run(
            "poetry",
            "run",
            "cdk",
            "-a",
            "python infrastructure/app.py",
            "deploy",
            "--require-approval",
            "never",
            env={"APP_MODE": env},
            external=True,
        )
    except Exception as e:
        session.error(f"🟥 CRITICAL: CDK deploy failed: {e}")


@nox.session
def push_config_to_ssm(session):
    """Sync environment config to AWS SSM Parameter Store."""
    ensure_bootstrap(session)
    env = get_env(session)
    config_path = Path(f"config/{env}.yaml")
    if not config_path.exists():
        session.skip(
            f"🟨 CAUTION: Config file not found: {config_path}. Skipping push_config_to_ssm step."
        )
        return
    session.run(
        "poetry",
        "run",
        "python",
        "scripts/config_to_ssm.py",
        "--env",
        env,
        external=True,
    )
