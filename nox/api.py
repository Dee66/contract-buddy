import os
from pathlib import Path
import nox
from utils import ensure_bootstrap, nox_logger, get_env


@nox.session
def run_api(session):
    """Run the API server for a given environment."""
    ensure_bootstrap(session)
    env = get_env(session)
    if not Path("src/adapters/api/main.py").exists():
        nox_logger.error(
            "🟥 CRITICAL: API entrypoint not found: src/adapters/api/main.py"
        )
        session.error("API entrypoint not found: src/adapters/api/main.py")
    nox_logger.info(f"🟦 NOTE: Starting API server in env: {env}")
    session.run(
        "poetry",
        "run",
        "uvicorn",
        "src.adapters.api.main:app",
        "--reload",
        env={"APP_MODE": env, "AWS_REGION": os.environ.get("AWS_REGION", "af-south-1")},
        external=True,
    )


@nox.session
def run_ingestion(session):
    """Run the RAG ingestion pipeline for a given environment."""
    ensure_bootstrap(session)
    env = get_env(session)
    config_path = f"config/{env}.yaml"
    if not Path(config_path).exists():
        nox_logger.error(f"🟥 CRITICAL: Config file not found: {config_path}")
        session.error(f"Config file not found: {config_path}")
    nox_logger.info(f"🟦 NOTE: Running ingestion for env: {env}")
    session.run(
        "poetry",
        "run",
        "python",
        "scripts/run_rag_ingestion.py",
        "--config",
        config_path,
        external=True,
    )
