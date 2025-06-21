import os
import sys
import logging

# Ensure the src directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.adapters.environment import setup_logging, get_config
from src.application.services.ingestion_service import IngestionService
from src.adapters.factories.factories import (
    create_data_source,
    create_chunking_strategy,
    create_embedding_service,
    create_vector_repository,
)


def main():
    """
    The main entry point for the data ingestion pipeline.
    This script orchestrates the entire process based on the central configuration.
    """
    setup_logging()
    config = get_config()
    logging.info("Starting RAG ingestion pipeline...")

    try:
        # 1. Use factories to construct adapters based on config
        data_source = create_data_source(config["data_source"])
        chunking_strategy = create_chunking_strategy(config["chunking_strategy"])
        embedding_service = create_embedding_service(config["embedding_service"])
        vector_repository = create_vector_repository(config["vector_repository"])

        # 2. Instantiate the application service with the adapters
        ingestion_service = IngestionService(
            data_source=data_source,
            chunking_strategy=chunking_strategy,
            embedding_service=embedding_service,
            vector_repository=vector_repository,
        )

        # 3. Execute the primary use case
        ingestion_service.ingest()

        logging.info("RAG ingestion pipeline completed successfully.")

    except Exception as e:
        logging.critical(
            f"A critical error occurred during the ingestion pipeline: {e}",
            exc_info=True,
        )
        # In a real MLOps pipeline, this would trigger an alert.


if __name__ == "__main__":
    """
    Entrypoint for running the RAG data ingestion pipeline as a script.
    This allows it to be called consistently from orchestration tools.
    """
    main()
