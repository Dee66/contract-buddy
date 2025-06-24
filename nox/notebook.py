import nox
from utils import ensure_bootstrap


@nox.session
def notebook(session):
    """Install notebook dependencies and launch Jupyter Lab."""
    ensure_bootstrap(session)
    session.run("poetry", "run", "jupyter", "lab", external=True)
