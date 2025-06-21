import os
import sys
import logging
import yaml
import json
from pathlib import Path

# Calculate the project root once, making all file paths relative to it.
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()


class JsonFormatter(logging.Formatter):
    """Formats log records as a single line of JSON."""

    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "message": record.getMessage(),
            "source": record.name,
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


def get_mode() -> str:
    """
    Returns the current run mode: 'dev' (default), 'staging', or 'prod'.
    Priority: ENV var CB_ENV > ENV var MODE > 'dev'
    """
    return os.environ.get("CB_ENV", os.environ.get("MODE", "dev")).lower()


def setup_logging():
    """
    Configures root logger for JSON output.
    Removes existing handlers to prevent duplicate logs.
    """
    # Remove any existing handlers to avoid duplicate logs in different contexts
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    log_level_str = os.environ.get("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    logging.basicConfig(level=log_level, handlers=[handler])
    logging.info(f"Logging initialized with level {log_level_str}")


def get_config(config_path: str = None) -> dict:
    """
    Loads YAML config. Defaults to 'config.yaml' in the project root.
    """
    if config_path is None:
        config_path = PROJECT_ROOT / "config.yaml"

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {config_path}")
        return {}
    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML file {config_path}: {e}")
        return {}
