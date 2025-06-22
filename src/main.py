import sys
import logging
from pathlib import Path
from src.adapters.environment import ConfigLoader, setup_logging
from src.application.services import IngestionService
from src.adapters.factories.factories import (
    create_chunking_strategy,
    create_data_source,
    create_vector_repository,
    create_embedding_service,
)


def main() -> int:
    """
    Main entrypoint for the RAG ingestion pipeline.
    This function acts as the Composition Root for the ingestion process.
    Returns 0 on success, 1 on failure.
    """
    try:
        setup_logging()
        logging.info("RAG ingestion pipeline starting...")

        config_loader = ConfigLoader()
        config = config_loader.get_config()

        # --- Defensive Programming: Ensure directories exist ---
        # Only create local data directories if a file_system source is used.
        if config.data_source.type == "file_system":
            Path(config.data_source.path).mkdir(parents=True, exist_ok=True)

        # The vector store path is always local to the container, so it always needs to exist.
        Path(config.vector_repository.persist_path).parent.mkdir(
            parents=True, exist_ok=True
        )
        # ---

        # The Composition Root passes the specific sub-configuration to each factory.
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
