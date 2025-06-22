import os
import logging

from src.adapters.data_sources.file_system_data_source import FileSystemDataSource
from src.adapters.data_sources.s3_data_source import S3DataSource
from src.adapters.chunking.langchain_chunking_strategy import LangchainChunkingStrategy
from src.adapters.embedding.bedrock_embedding_service import BedrockEmbeddingService
from src.adapters.embedding.sentence_transformer_embedding_service import (
    SentenceTransformerEmbeddingService,
)
from src.adapters.vector_storage.faiss_vector_repository import FaissVectorRepository
from src.domain.ports import (
    ChunkingStrategy,
    DataSource,
    EmbeddingService,
    VectorRepository,
)
from src.domain.entities.config import (
    ChunkingStrategyConfig,
    DataSourceConfig,
    EmbeddingServiceConfig,
    VectorRepositoryConfig,
)


def create_data_source(config: DataSourceConfig) -> DataSource:
    """Factory for creating a data source from its specific configuration."""
    logging.info(f"Creating data source of type: {config.type}")
    if config.type == "file_system":
        return FileSystemDataSource(path=config.path)
    if config.type == "s3":
        return S3DataSource(bucket=config.bucket, prefix=config.prefix)
    raise ValueError(f"Unsupported data source type: {config.type}")


def create_chunking_strategy(config: ChunkingStrategyConfig) -> ChunkingStrategy:
    """Factory for creating a chunking strategy from its specific configuration."""
    logging.info(f"Creating chunking strategy of type: {config.type}")
    if config.type == "langchain":
        return LangchainChunkingStrategy(
            chunk_size=config.chunk_size, chunk_overlap=config.chunk_overlap
        )
    raise ValueError(f"Unsupported chunking strategy type: {config.type}")


def create_embedding_service(config: EmbeddingServiceConfig) -> EmbeddingService:
    """Factory for creating an embedding service from its specific configuration."""
    logging.info(f"Creating embedding service of type: {config.type}")
    if config.type == "bedrock":
        return BedrockEmbeddingService(
            aws_region=os.environ.get("AWS_REGION", config.aws_region),
            model_id=config.model_id,
        )
    if config.type == "sentence_transformer":
        return SentenceTransformerEmbeddingService(model_name=config.model_name)
    raise ValueError(f"Unsupported embedding service type: {config.type}")


def create_vector_repository(
    config: VectorRepositoryConfig, embedding_service: EmbeddingService
) -> VectorRepository:
    """
    Factory for creating a vector repository from its specific configuration.
    """
    if config.type == "faiss":
        return FaissVectorRepository(
            persist_path=config.persist_path,
            embedding_dim=embedding_service.get_dimension(),
            s3_bucket=config.s3_bucket,
            s3_key=config.s3_key,
        )
    raise ValueError(f"Unknown vector repository type: {config.type}")
