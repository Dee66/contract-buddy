import os
import json
from typing import Any, Dict, Optional

import boto3
from pydantic import BaseModel


# --- Pydantic schema for config validation ---
class AppConfig(BaseModel):
    vector_store_bucket: str
    data_bucket: str
    log_level: str = "INFO"
    api_timeout_seconds: int = 30
    feature_flags: Dict[str, Any] = {}


class ConfigManager:
    """
    Loads and validates application configuration from AWS SSM Parameter Store.
    Fails fast if config is missing or malformed.
    Exposes config version for observability.
    """

    def __init__(self, env_var: str = "APP_MODE"):
        self.env = os.environ.get(env_var)
        if not self.env:
            raise RuntimeError(f"Missing required environment variable: {env_var}")
        self.ssm_param = f"/codecraft-ai/{self.env}/AppConfig"
        self._config: Optional[AppConfig] = None
        self.last_version: Optional[str] = None

    def load(self, force_reload: bool = False) -> AppConfig:
        if self._config is not None and not force_reload:
            return self._config

        ssm = boto3.client("ssm", region_name=os.environ.get("AWS_REGION"))
        try:
            response = ssm.get_parameter(Name=self.ssm_param, WithDecryption=True)
            raw = response["Parameter"]["Value"]
            self.last_version = str(response["Parameter"].get("Version", "unknown"))
            data = json.loads(raw)
            self._config = AppConfig(**data)
            # Emit config version as a log/metric for observability
            print(f'[METRIC] config_version{{env="{self.env}"}} {self.last_version}')
            return self._config
        except Exception as e:
            print(f'[METRIC] config_validation_failure{{env="{self.env}"}} 1')
            raise RuntimeError(
                f"Failed to load or validate config from {self.ssm_param}: {e}"
            )

    @property
    def config(self) -> AppConfig:
        if self._config is None:
            return self.load()
        return self._config

    def get_current_api_key(self) -> Optional[str]:
        # Example: fetch API key from env or secrets manager for reload endpoint auth
        return os.environ.get("API_KEY")
