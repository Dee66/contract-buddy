import nox
from cdk import cdk_diff, push_config_to_ssm
from docker import docker_build_all, docker_compose_down, docker_compose_up

# from ml import retrain_model, sagemaker_train, sync_artifacts_to_s3
from test import smoke_test_api, validate_notebooks
from utils import nox_logger, get_env


def get_now():
    import datetime

    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@nox.session
def all(session):
    """
    Run all critical checks and builds for a production-grade, AWS-native workflow.
    🟪 ARCH: Skips non-critical steps (e.g., infra) as warnings, does not abort pipeline on session.skip().
    """
    session.notify("bootstrap")
    env = get_env(session)
    nox_logger.info(f"🟦 NOTE: Starting 'all' session for env: {env}")

    critical_steps = [
        docker_build_all,
        docker_compose_up,
        smoke_test_api,
        docker_compose_down,
        cdk_diff,
        push_config_to_ssm,
        validate_notebooks,
        # retrain_model,
        # sagemaker_train,
        # sync_artifacts_to_s3,
    ]
    for step_func in critical_steps:
        step_name = step_func.__name__
        nox_logger.info(
            f"🟦 NOTE: [{get_now()}] Running step: {step_name} (env: {env})"
        )
        try:
            step_func(session)
            nox_logger.info(
                f"🟩 GOOD: Step '{step_name}' completed successfully in env '{env}'."
            )
        except nox.sessions._SessionSkip as skip_exc:
            nox_logger.warning(f"🟨 CAUTION: Step '{step_name}' skipped: {skip_exc}")
            continue  # 🟪 ARCH: Continue pipeline on skip
        except Exception as exc:
            nox_logger.error(
                f"🟥 CRITICAL: [{get_now()}] Step '{step_name}' failed in env '{env}': {exc}\n"
                "🟨 CAUTION: Aborting pipeline due to critical failure. No further steps will be executed."
            )
            session.error(
                f"🟥 CRITICAL: [{get_now()}] Step '{step_name}' failed in env '{env}': {exc}\n"
                "🟨 CAUTION: Aborting pipeline due to critical failure. No further steps will be executed."
            )
            break
