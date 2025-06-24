import nox
from utils import ensure_bootstrap, nox_logger


@nox.session
def bootstrap(session):
    """
    🟩 GOOD: Bootstrap session for environment setup.
    Installs base dependencies and prepares the environment for all other sessions.
    """
    ensure_bootstrap(session)
    nox_logger.info("🟦 NOTE: Running bootstrap session: installing base dependencies.")
    session.run("poetry", "install", external=True)
