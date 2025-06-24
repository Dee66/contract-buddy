# tests/scripts/test_validate_config.py

import pytest
from pydantic import ValidationError
from scripts.validate_config import AppConfig, AppSecrets


@pytest.mark.parametrize(
    "config_dict",
    [
        {
            "vector_store_bucket": "bucket",
            "data_bucket": "bucket",
            "log_level": "INFO",
            "api_timeout_seconds": 30,
            "feature_flags": {},
            "data_source": {
                "type": "s3",
            },
            "embedding_service": {
                "type": "bedrock",
            },
            "vector_repository": {
                "type": "faiss",
            },
        },
    ],
)
def test_app_config_valid(config_dict):
    cfg = AppConfig(**config_dict)
    assert cfg.vector_store_bucket == "bucket"


@pytest.mark.parametrize(
    "config_dict",
    [
        {
            # Missing required field
            "data_bucket": "bucket",
            "log_level": "INFO",
            "api_timeout_seconds": 30,
            "feature_flags": {},
        },
    ],
)
def test_app_config_invalid(config_dict):
    with pytest.raises(ValidationError):
        AppConfig(**config_dict)


@pytest.mark.parametrize(
    "secret_dict",
    [
        {
            "DB_HOST": "host",
            "DB_PORT": "5432",
            "DB_USERNAME": "user",
            "DB_PASSWORD": "pw",
            "DB_NAME": "db",
            "S3_BUCKET_NAME": "bucket",
            "S3_REGION": "af-south-1",
            "API_KEY": "key",
            "API_ENDPOINT": "endpoint",
            "LOG_LEVEL": "DEBUG",
            "MONITORING_ENDPOINT": "endpoint",
            "ENCRYPTION_KEY": "key",
            "JWT_SECRET": "jwt",
            "MODEL_REGISTRY_URL": "url",
            "MODEL_VERSION": "v1",
            "COST_TRACKING_ID": "id",
            "TRACING_ENDPOINT": "endpoint",
        },
    ],
)
def test_app_secrets_valid(secret_dict):
    secrets = AppSecrets(**secret_dict)
    assert secrets.DB_HOST == "host"


@pytest.mark.parametrize(
    "secret_dict",
    [
        {
            # Missing required field
            "DB_HOST": "host",
            "DB_PORT": "5432",
            # ...other fields omitted...
        },
    ],
)
def test_app_secrets_invalid(secret_dict):
    with pytest.raises(ValidationError):
        AppSecrets(**secret_dict)
