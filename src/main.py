import sys
import logging
from pathlib import Path
from fastapi import FastAPI, Depends
from src.adapters.config_manager import ConfigManager
from src.application.services import IngestionService
from src.adapters.factories.factories import (
    create_chunking_strategy,
    create_data_source,
    create_vector_repository,
    create_embedding_service,
)

app = FastAPI()

# Instantiate ConfigManager at startup
config_manager = ConfigManager()


@app.on_event("startup")
def load_config():
    # Load and validate config at startup; fail fast if invalid
    config_manager.load()


def get_app_config():
    return config_manager.config


@app.get("/config")
def show_config(cfg=Depends(get_app_config)):
    # Expose config for debugging (remove or secure in production)
    return cfg.dict()


def main() -> int:
    """
    Main entrypoint for the RAG ingestion pipeline.
    This function acts as the Composition Root for the ingestion process.
    Returns 0 on success, 1 on failure.
    """
    try:
        # Use config from ConfigManager (SSM Parameter Store)
        config = config_manager.config

        # Defensive Programming: Ensure directories exist if needed
        # (Assuming config has data_source and vector_repository keys as before)
        # You may need to adapt this if your config structure changes.
        # Example assumes config is a Pydantic model with .dict() support.
        if (
            hasattr(config, "data_source")
            and getattr(config.data_source, "type", None) == "file_system"
        ):
            Path(config.data_source.path).mkdir(parents=True, exist_ok=True)
        if hasattr(config, "vector_repository"):
            Path(config.vector_repository.persist_path).parent.mkdir(
                parents=True, exist_ok=True
            )

        # Compose pipeline using config
        data_source = create_data_source(config.data_source)
        chunking_strategy = create_chunking_strategy(config.chunking_strategy)
        embedding_service = create_embedding_service(config.embedding_service)
        vector_repository = create_vector_repository(
            config.vector_repository, embedding_service
        )

        ingestion_service = IngestionService(
            data_source=data_source,
            chunking_strategy=chunking_strategy,
            embedding_service=embedding_service,
            vector_repository=vector_repository,
        )

        ingestion_service.ingest()

        logging.info("RAG ingestion pipeline finished successfully.")
        return 0

    except Exception as e:
        logging.critical(f"Ingestion pipeline failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
