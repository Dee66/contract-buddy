import subprocess
import nox
from utils import ensure_bootstrap, nox_logger


@nox.session
def security_scan(session):
    """Run security audits on dependencies and source code."""
    ensure_bootstrap(session)
    nox_logger.info("🟦 NOTE: Running pip-audit for dependency vulnerability scan...")
    result = subprocess.run(
        ["poetry", "run", "pip-audit"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        nox_logger.error(
            f"🟥 CRITICAL: pip-audit found vulnerabilities:\n"
            f"{result.stdout or ''}{result.stderr or ''}\n"
            "🟨 CAUTION: One or more dependencies have known vulnerabilities. "
            "Review the above output and update your dependencies in pyproject.toml. "
            "Do not deploy to production until all critical vulnerabilities are resolved."
        )
        session.error(
            f"🟥 CRITICAL: pip-audit found vulnerabilities:\n"
            f"{result.stdout or ''}{result.stderr or ''}\n"
            "🟨 CAUTION: One or more dependencies have known vulnerabilities. "
            "Review the above output and update your dependencies in pyproject.toml. "
            "Do not deploy to production until all critical vulnerabilities are resolved."
        )
    nox_logger.info("🟩 GOOD: pip-audit completed. No known vulnerabilities found.")

    try:
        session.run("poetry", "run", "bandit", "-r", "src/", external=True)
        nox_logger.info("🟩 GOOD: Bandit security scan completed successfully.")
    except Exception as e:
        nox_logger.error(
            f"🟥 CRITICAL: Bandit security scan failed: {e}", exc_info=True
        )
        session.error(f"🟥 CRITICAL: Bandit security scan failed: {e}")


# @nox.session
# def lint(session):
#     """Run the linter and formatter."""
#     ensure_bootstrap(session)
#     try:
#         session.run("poetry", "run", "ruff", "check", ".", "--fix", external=True)
#         session.run("poetry", "run", "ruff", "format", ".", external=True)
#     except Exception as e:
#         session.error(f"🟥 CRITICAL: Linting failed: {e}")
