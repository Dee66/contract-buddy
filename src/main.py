import sys
import logging
from src.adapters.environment import setup_logging, get_config
from src.application.services import IngestionService
from src.adapters.factories.factories import (
    create_chunking_strategy,
    create_data_source,
    create_vector_repository,
    create_embedding_service,
)


def main():
    """
    Main entrypoint for the application container.

    This function acts as the Composition Root. It initializes application-wide
    configurations, instantiates and wires together all components (Dependency Injection),
    and then invokes the primary business logic. It includes a top-level exception
    handler to ensure any critical failures are logged before the container exits.
    """
    try:
        # 1. Setup: Initialize logging and load configuration
        setup_logging()
        logging.info("Application container starting...")
        config = get_config()

        # 2. Dependency Injection via Factories
        data_source = create_data_source(config)
        chunking_strategy = create_chunking_strategy(config)
        embedding_service = create_embedding_service(config)
        vector_repository = create_vector_repository(config)

        # 3. Application Instantiation
        ingestion_service = IngestionService(
            data_source=data_source,
            chunking_strategy=chunking_strategy,
            embedding_service=embedding_service,
            vector_repository=vector_repository,
        )

        # 4. Execution
        ingestion_service.ingest()

        logging.info("Application container finished successfully.")
        sys.exit(0)

    except Exception as e:
        logging.critical(
            f"Application failed with a critical error: {e}", exc_info=True
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
