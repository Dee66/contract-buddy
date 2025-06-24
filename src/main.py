import sys
import logging
from pathlib import Path
from fastapi import FastAPI, Depends  # type: ignore
from src.adapters.config_manager import ConfigManager
from src.application.services import IngestionService
from src.adapters.factories.factories import (
    create_chunking_strategy,
    create_data_source,
    create_vector_repository,
    create_embedding_service,
)

app = FastAPI()

config_manager = ConfigManager()


@app.on_event("startup")
def load_config():
    config_manager.load()


def get_app_config():
    return config_manager.config


@app.get("/config")
def show_config(cfg=Depends(get_app_config)):
    return cfg.dict()


def main() -> int:
    try:
        config = config_manager.config

        # 🟨 CAUTION: Defensive directory creation assumes config fields exist and are correct types.
        if (
            hasattr(config, "data_source")
            and isinstance(config.data_source, dict)
            and config.data_source.get("type") == "file_system"
        ):
            Path(config.data_source.get("path", "./data")).mkdir(
                parents=True, exist_ok=True
            )
        if hasattr(config, "vector_repository") and isinstance(
            config.vector_repository, dict
        ):
            Path(
                config.vector_repository.get("persist_path", "./vector_store")
            ).parent.mkdir(parents=True, exist_ok=True)

        data_source = create_data_source(config.data_source.get("type"))  # type: ignore
        chunking_strategy = create_chunking_strategy(
            config.chunking_strategy.get("type"),
            config.chunking_strategy.get("chunk_overlap", 0),
        )  # type: ignore
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
