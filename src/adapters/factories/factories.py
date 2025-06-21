import os
import logging
from typing import Dict, Any

from src.adapters.data_sources.file_system_data_source import FileSystemDataSource
from src.adapters.chunking.langchain_chunking_strategy import LangchainChunkingStrategy
from src.adapters.embedding.bedrock_embedding_service import BedrockEmbeddingService
from src.adapters.vector_storage.faiss_vector_repository import FaissVectorRepository
from src.domain.ports import (
    IDataSource,
    IChunkingStrategy,
    IEmbeddingService,
    IVectorRepository,
)


def create_data_source(config: dict) -> IDataSource:
    """Factory function to create a data source based on configuration."""
    source_type = config["type"]
    logging.info(f"Creating data source of type: {source_type}")
    if source_type == "file_system":
        path = config["path"]
        os.makedirs(path, exist_ok=True)
        return FileSystemDataSource(path=path)
    else:
        raise ValueError(f"Unsupported data source type: {source_type}")


def create_chunking_strategy(config: Dict[str, Any]) -> IChunkingStrategy:
    """Factory function to create a chunking strategy based on configuration."""
    strategy_type = config["type"]
    logging.info(f"Creating chunking strategy of type: {strategy_type}")
    if strategy_type == "langchain":
        return LangchainChunkingStrategy(
            chunk_size=config["chunk_size"], chunk_overlap=config["chunk_overlap"]
        )
    else:
        raise ValueError(f"Unsupported chunking strategy type: {strategy_type}")


def create_embedding_service(config: Dict[str, Any]) -> IEmbeddingService:
    """Factory function to create an embedding service based on configuration."""
    service_type = config["type"]
    logging.info(f"Creating embedding service of type: {service_type}")
    if service_type == "bedrock":
        return BedrockEmbeddingService(
            aws_region=os.environ.get("AWS_REGION", config.get("aws_region")),
            model_id=config.get("model_id"),
        )
    else:
        raise ValueError(f"Unsupported embedding service type: {service_type}")


def create_vector_repository(config: Dict[str, Any]) -> IVectorRepository:
    """Factory function to create a vector repository based on configuration."""
    repo_type = config["type"]
    logging.info(f"Creating vector repository of type: {repo_type}")
    if repo_type == "faiss":
        embedding_dim = config["embedding_dim"]
        persist_path = config["persist_path"]
        return FaissVectorRepository(
            embedding_dim=embedding_dim, persist_path=persist_path
        )
    else:
        raise ValueError(f"Unsupported vector repository type: {repo_type}")
