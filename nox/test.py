from pathlib import Path
import nox
from utils import ensure_bootstrap, nox_logger


@nox.session
def test(session):
    """Run the full test suite with coverage and type checks."""
    ensure_bootstrap(session)
    nox_logger.info("🟦 NOTE: Starting test session.")
    try:
        session.run(
            "poetry",
            "run",
            "pytest",
            "--cov=src",
            "--cov-report=term-missing",
            external=True,
        )
        session.run("poetry", "run", "mypy", "src", external=True)
        nox_logger.info("Test session completed successfully.")
    except Exception as e:
        nox_logger.error(
            f"🟥 CRITICAL: Tests or type checks failed: {e}", exc_info=True
        )
        session.error(f"🟥 CRITICAL: Tests or type checks failed: {e}")


@nox.session
def smoke_test_api(session):
    """Run API smoke tests after build/deploy."""
    ensure_bootstrap(session)
    if not Path("tests/test_api_smoke.py").exists():
        session.log("WARNING: Smoke test file not found: tests/test_api_smoke.py")
        return
    session.run("poetry", "run", "pytest", "tests/test_api_smoke.py", external=True)


@nox.session
def validate_notebooks(session):
    """Run nbval to validate all Jupyter notebooks (CI/CD, reproducibility)."""
    ensure_bootstrap(session)
    if not Path("notebooks").exists():
        session.log(
            "WARNING: No notebooks directory found, skipping notebook validation."
        )
        return
    session.run("poetry", "run", "pytest", "--nbval", "notebooks/", external=True)
