import os
import sys
import logging
import yaml
import json
from logging.handlers import RotatingFileHandler
from pathlib import Path
from pydantic import ValidationError

from src.domain.entities.config import AppConfig


# --- Constants ---
PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", Path(__file__).parent.parent.parent))
LOG_DIR = PROJECT_ROOT / "logs"
DEFAULT_CONFIG_DIR = PROJECT_ROOT / "config"


class ConfigLoader:
    """
    A class to manage loading and merging of configuration files.
    Encapsulates configuration logic, making it explicit and testable.
    """

    def __init__(self, config_dir: Path = DEFAULT_CONFIG_DIR):
        self.config_dir = config_dir
        self.mode = os.environ.get("APP_MODE", "dev").lower()

    def _deep_merge(self, base: dict, override: dict) -> dict:
        """Recursively merges two dictionaries."""
        result = base.copy()
        for key, value in override.items():
            if (
                isinstance(value, dict)
                and key in result
                and isinstance(result[key], dict)
            ):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    def get_config(self) -> AppConfig:
        """
        Loads configuration from YAML files and overrides with environment variables.
        """
        base_config_path = self.config_dir / "base.yaml"
        mode_config_path = self.config_dir / f"{self.mode}.yaml"

        try:
            with open(base_config_path, "r") as f:
                config_dict = yaml.safe_load(f)
        except FileNotFoundError:
            logging.error(f"Base configuration file not found at {base_config_path}")
            raise
        except yaml.YAMLError as e:
            logging.error(f"Error parsing base configuration file: {e}")
            raise

        if mode_config_path.exists():
            try:
                with open(mode_config_path, "r") as f:
                    mode_config = yaml.safe_load(f)
                if mode_config:
                    config_dict = self._deep_merge(config_dict, mode_config)
            except yaml.YAMLError as e:
                logging.error(f"Error parsing mode-specific configuration file: {e}")
                raise

        # --- Environment Variable Override ---
        # This is the crucial step for cloud deployments.
        if "DATA_BUCKET" in os.environ:
            config_dict["data_source"]["bucket"] = os.environ["DATA_BUCKET"]
        if "VECTOR_STORE_BUCKET" in os.environ:
            config_dict["vector_repository"]["s3_bucket"] = os.environ[
                "VECTOR_STORE_BUCKET"
            ]

        try:
            return AppConfig.model_validate(config_dict)
        except ValidationError as e:
            logging.error(f"Configuration validation failed:\n{e}")
            raise


# --- Standalone Functions (remain for convenience) ---


class JsonFormatter(logging.Formatter):
    """Custom formatter to output logs in JSON format."""

    def format(self, record):
        # Get the application mode for contextual logging
        app_mode = os.environ.get("APP_MODE", "dev").lower()
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "mode": app_mode,
            "message": record.getMessage(),
            "source": record.name,
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


def setup_logging():
    """Configures logging for the application idempotently."""
    root_logger = logging.getLogger()

    # Use a custom attribute to ensure this setup runs only once.
    if getattr(root_logger, "_configured", False):
        return

    os.makedirs(LOG_DIR, exist_ok=True)
    log_file = LOG_DIR / "app.log"

    root_logger.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JsonFormatter())
    root_logger.addHandler(console_handler)

    # File handler
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=5
    )
    file_handler.setFormatter(JsonFormatter())
    root_logger.addHandler(file_handler)

    root_logger._configured = True
    logging.info("Logging initialized with level INFO")
