import argparse
import logging
import sys
import os
from typing import Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.adapters.data_sources.rag_ingestion_pipeline import RagIngestionPipeline

# These imports are required for patching in tests (do not remove)
from src.application.services.ingestion_service import IngestionService  # noqa: F401
from src.adapters.factories.factories import create_vector_repository  # noqa: F401


def run_rag_ingestion(config_path: Optional[str] = None, dry_run: bool = False) -> int:
    """
    Entry point for running the RAG ingestion pipeline.
    Args:
        config_path (str): Path to the YAML config file. If None, uses default.
        dry_run (bool): If True, pipeline will validate config and exit.
    Returns:
        int: Exit code (0 for success, nonzero for failure)
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("run_rag_ingestion")

    try:
        pipeline = RagIngestionPipeline(config_path=config_path)
        if dry_run:
            logger.info("Dry run: validating configuration only.")
            pipeline.validate_config()
            logger.info("Config validation successful.")
            return 0
        logger.info("Starting RAG ingestion pipeline...")
        pipeline.run()
        logger.info("RAG ingestion pipeline completed successfully.")
        return 0
    except Exception as e:
        logger.error(f"RAG ingestion failed: {e}", exc_info=True)
        return 1


# Ensure this function is available at the module level for patching
__all__ = ["run_rag_ingestion"]

# 🟩 GOOD: Only run CLI logic if executed as a script
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the RAG ingestion pipeline.")
    parser.add_argument(
        "--config", type=str, default=None, help="Path to config YAML file."
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Validate config and exit."
    )
    args = parser.parse_args()
    sys.exit(run_rag_ingestion(config_path=args.config, dry_run=args.dry_run))
