import os
import logging
import yaml
import json

def get_mode() -> str:
    """
    Returns the current run mode: 'dev' (default) or 'prod'.
    """
    return os.environ.get("MODE", "dev").lower()

class JsonFormatter(logging.Formatter):
    def format(self, record):
        # Format time to show only up to minutes
        log_record = {
            "ts": self.formatTime(record, "%Y-%m-%d %H:%M"),
            "msg": record.getMessage(),
            "mod": record.module,
            "func": record.funcName,
            "line": record.lineno,
        }
        return json.dumps(log_record)

def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logging.basicConfig(level=logging.INFO, handlers=[handler])

def get_config(config_path: str = "config.yaml") -> dict:
    """
    Loads YAML config from the given path.
    """
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)