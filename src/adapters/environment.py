# 🟪 ARCH: Environment adapter for config, logging, and mode detection.
import os
import logging
import sys
from typing import Optional
import yaml
from pydantic import ValidationError
from pathlib import Path
from src.domain.entities.config import AppConfig


# --- Constants ---
PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", Path(__file__).parent.parent.parent))
LOG_DIR = PROJECT_ROOT / "logs"
DEFAULT_CONFIG_DIR = PROJECT_ROOT / "config"


# 🟩 GOOD: Canonical logging setup for all environments.
def setup_logging(level: Optional[str] = None, json_format: bool = False) -> None:
    """
    🟩 GOOD: Canonical logging setup for all environments (dev, staging, prod).
    🟦 NOTE: Supports both plain and JSON log formatting for AWS-native observability.
    """
    log_level = level or os.environ.get("LOG_LEVEL", "INFO")
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    root_logger.handlers = []

    console_handler = logging.StreamHandler(sys.stdout)
    if json_format or os.environ.get("LOG_JSON", "0") == "1":

        class JsonFormatter(logging.Formatter):
            def format(self, record):
                import json

                log_record = {
                    "timestamp": self.formatTime(record, "%Y-%m-%d %H:%M:%S,%f")[:-3],
                    "level": record.levelname,
                    "mode": os.environ.get("ENV_MODE", "dev"),
                    "message": record.getMessage(),
                    "source": record.name,
                }
                return json.dumps(log_record)

        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    root_logger.info(f"Logging initialized with level {log_level}")


# 🟩 GOOD: Clean, testable environment mode detection.
def get_mode() -> str:
    """
    🟦 NOTE: Returns the current environment mode (dev, staging, prod).
    🟪 ARCH: Reads from ENV_MODE or defaults to 'dev' for local/test.
    """
    return os.environ.get("ENV_MODE", "dev")


# 🟩 GOOD: Canonical config loader for all environments.
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
        🟩 GOOD: Single, production-grade config loader for all environments.
        """
        base_config_path = self.config_dir / "dev.yaml"
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
        if "DATA_BUCKET" in os.environ:
            config_dict.setdefault("data_source", {})["bucket"] = os.environ[
                "DATA_BUCKET"
            ]
        if "VECTOR_STORE_BUCKET" in os.environ:
            config_dict.setdefault("vector_repository", {})["s3_bucket"] = os.environ[
                "VECTOR_STORE_BUCKET"
            ]

        try:
            return AppConfig.model_validate(config_dict)
        except ValidationError as e:
            logging.error(f"Configuration validation failed:\n{e}")
            raise
