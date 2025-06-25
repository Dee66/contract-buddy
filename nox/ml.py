import os
from pathlib import Path
import nox
from utils import ensure_bootstrap, nox_logger, get_env

# 🟪 ARCH: Always resolve config and script paths relative to the project root for reliability across all environments.


def project_root():
    # 🟪 ARCH: Returns the absolute project root, regardless of working directory.
    return Path(__file__).parent.parent.resolve()


@nox.session
def retrain_model(session):
    """Run model retraining pipeline for the selected environment."""
    nox_logger.info("🟦 NOTE: [retrain_model] Session started.")
    ensure_bootstrap(session)
    env = get_env(session)
    config_path = project_root() / "config" / f"{env}.yaml"
    script_path = project_root() / "scripts" / "peft_pipeline_runner.py"

    # 🟦 NOTE: Debugging output for path resolution and environment
    nox_logger.info(f"🟦 NOTE: [retrain_model] Project root: {project_root()}")
    nox_logger.info(
        f"🟦 NOTE: [retrain_model] Config path: {config_path} (exists: {config_path.exists()})"
    )
    nox_logger.info(
        f"🟦 NOTE: [retrain_model] Script path: {script_path} (exists: {script_path.exists()})"
    )
    nox_logger.info(
        f"🟦 NOTE: [retrain_model] Current working directory: {os.getcwd()}"
    )
    nox_logger.info(
        f"🟦 NOTE: [retrain_model] PYTHONPATH: {os.environ.get('PYTHONPATH', '')}"
    )

    if not config_path.exists():
        nox_logger.error(
            f"🟥 CRITICAL: Config file not found: {config_path.as_posix()}"
        )
        session.error(f"🟥 CRITICAL: Config file not found: {config_path.as_posix()}")
    if not script_path.exists():
        nox_logger.error(
            f"🟥 CRITICAL: Model retraining script not found: {script_path.as_posix()}"
        )
        session.error(
            f"🟥 CRITICAL: Model retraining script not found: {script_path.as_posix()}"
        )

    # 🟦 NOTE: Set PYTHONPATH to project root for src/ imports in subprocesses.
    pythonpath = os.environ.get("PYTHONPATH", "")
    new_pythonpath = (
        f"{project_root().as_posix()}{os.pathsep}{pythonpath}"
        if pythonpath
        else project_root().as_posix()
    )
    nox_logger.info(
        f"🟦 NOTE: [retrain_model] Using PYTHONPATH for subprocess: {new_pythonpath}"
    )

    nox_logger.info(
        f"🟦 NOTE: [retrain_model] Running: poetry run python {script_path.as_posix()} --config {config_path.as_posix()}"
    )
    session.run(
        "poetry",
        "run",
        "python",
        script_path.as_posix(),
        "--config",
        config_path.as_posix(),
        external=True,
        env={"PYTHONPATH": new_pythonpath, **os.environ},
    )
    nox_logger.info("[retrain_model] Session completed.")


@nox.session
def sagemaker_train(session):
    """
    Launch a SageMaker training job for the selected environment.
    Assumes you have a script: scripts/sagemaker_train.py
    """
    nox_logger.info("🟦 NOTE: [sagemaker_train] Session started.")
    ensure_bootstrap(session)
    env = get_env(session)
    config_path = project_root() / "config" / f"{env}.yaml"
    script_path = project_root() / "scripts" / "sagemaker_train.py"
    nox_logger.info(
        f"🟦 NOTE: [sagemaker_train] Config path: {config_path} (exists: {config_path.exists()})"
    )
    nox_logger.info(
        f"🟦 NOTE: [sagemaker_train] Script path: {script_path} (exists: {script_path.exists()})"
    )
    if not script_path.exists():
        nox_logger.error(
            f"🟥 CRITICAL: SageMaker training script not found: {script_path.as_posix()}"
        )
        session.error(f"SageMaker training script not found: {script_path.as_posix()}")
    if not config_path.exists():
        nox_logger.error(
            f"🟥 CRITICAL: Config file not found: {config_path.as_posix()}"
        )
        session.error(f"Config file not found: {config_path.as_posix()}")

    pythonpath = os.environ.get("PYTHONPATH", "")
    new_pythonpath = (
        f"{project_root().as_posix()}{os.pathsep}{pythonpath}"
        if pythonpath
        else project_root().as_posix()
    )
    nox_logger.info(
        f"🟦 NOTE: [sagemaker_train] Using PYTHONPATH for subprocess: {new_pythonpath}"
    )
    session.run(
        "poetry",
        "run",
        "python",
        script_path.as_posix(),
        "--config",
        config_path.as_posix(),
        external=True,
        env={"PYTHONPATH": new_pythonpath, **os.environ},
    )
    nox_logger.info("[sagemaker_train] Session completed.")


@nox.session
def sync_artifacts_to_s3(session):
    """
    Sync model artifacts or data to S3 for the selected environment.
    """
    nox_logger.info("🟦 NOTE: [sync_artifacts_to_s3] Session started.")
    ensure_bootstrap(session)
    env = get_env(session)
    bucket = os.environ.get("ARTIFACT_BUCKET")
    if not bucket:
        nox_logger.error("🟥 CRITICAL: ARTIFACT_BUCKET environment variable not set.")
        session.error("ARTIFACT_BUCKET environment variable not set.")
    local_dir = project_root() / "artifacts"
    nox_logger.info(
        f"🟦 NOTE: [sync_artifacts_to_s3] Local artifacts dir: {local_dir} (exists: {local_dir.exists()})"
    )
    if not local_dir.exists():
        nox_logger.error(
            f"🟥 CRITICAL: Artifacts directory not found: {local_dir.as_posix()}"
        )
        session.error(f"Artifacts directory not found: {local_dir.as_posix()}")
    s3_prefix = f"s3://{bucket}/{env}/artifacts/"
    nox_logger.info(f"🟦 NOTE: [sync_artifacts_to_s3] Syncing to: {s3_prefix}")
    session.run("aws", "s3", "sync", local_dir.as_posix(), s3_prefix, external=True)
    nox_logger.info("[sync_artifacts_to_s3] Session completed.")
