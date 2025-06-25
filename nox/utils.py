import os
import logging
import json


def setup_nox_logging():
    import sys
    from pathlib import Path

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "nox.log"

    logger = logging.getLogger("nox")
    logger.setLevel(logging.INFO)

    if getattr(logger, "_configured", False):
        return logger

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(
        logging.Formatter(
            "[%(asctime)s] %(levelname)s [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    logger.addHandler(ch)

    class JsonFormatter(logging.Formatter):
        def format(self, record):
            log_record = {
                "timestamp": self.formatTime(record, self.datefmt),
                "level": record.levelname,
                "env": os.environ.get("APP_MODE", "dev"),
                "session": record.name,
                "message": record.getMessage(),
            }
            if record.exc_info:
                log_record["exception"] = self.formatException(record.exc_info)
            return json.dumps(log_record)

    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)
    fh.setFormatter(JsonFormatter())
    logger.addHandler(fh)

    logger._configured = True
    return logger


nox_logger = setup_nox_logging()


def ensure_bootstrap(session):
    # No-op if bootstrap already ran in this env
    pass


# 🟪 ARCH: Centralized, production-grade logging for all Nox sessions.


def get_env(session):
    """
    Returns the current environment name for the session.
    Defaults to 'dev' if not set.
    """
    # Priority: session positional args > env var > default
    if session.posargs:
        return session.posargs[0]
    return os.environ.get("APP_MODE", "dev")


nox_logger = setup_nox_logging()
