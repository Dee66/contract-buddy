import os
import sys
import logging
import argparse

# 🟦 NOTE: Ensure the src directory is in the Python path for all environments
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# 🟩 GOOD: Use the canonical config and logging setup for the whole repo
from src.adapters.environment import setup_logging, ConfigLoader

from src.application.services.query_service import QueryService
from src.adapters.factories.factories import (
    create_embedding_service,
    create_vector_repository,
)


def main():
    """
    Command-line interface for querying the knowledge base.
    This acts as the Composition Root for the query use case.
    """
    parser = argparse.ArgumentParser(
        description="Query the CodeCraft AI knowledge base."
    )
    parser.add_argument("query", type=str, help="The query string to search for.")
    parser.add_argument(
        "--top-k", type=int, default=3, help="The number of results to retrieve."
    )
    args = parser.parse_args()

    try:
        # 1. Setup
        setup_logging()
        config = ConfigLoader().get_config().rag_pipeline

        # 2. Dependency Injection via Factories
        embedding_service = create_embedding_service(config)
        vector_repository = create_vector_repository(
            config["vector_store"], config["embedding_dimension"]
        )

        # 3. Application Instantiation
        query_service = QueryService(
            embedding_service=embedding_service, vector_repository=vector_repository
        )

        # 4. Execution
        results = query_service.search(query=args.query, top_k=args.top_k)

        # 5. Display Results
        print("\n--- Query Results ---")
        if not results:
            print("No results found.")
        else:
            for i, chunk in enumerate(results):
                print(f"\n--- Result {i + 1} ---")
                print(f"Source: {chunk.metadata.get('source_location', 'N/A')}")
                print("Content:")
                print(chunk.content)
        print("\n---------------------\n")

    except Exception as e:
        logging.critical(f"Query failed with a critical error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
