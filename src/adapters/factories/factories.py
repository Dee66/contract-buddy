from typing import Optional, Literal, Any
from src.adapters.data_sources.file_system_data_source import FileSystemDataSource
from src.adapters.data_sources.s3_data_source import S3DataSource
from src.adapters.chunking.langchain_chunking_strategy import LangchainChunkingStrategy
from src.adapters.vector_storage.faiss_vector_repository import FaissVectorRepository
from src.domain.ports import IEmbeddingService
from src.adapters.embedding.bedrock_embedding_service import BedrockEmbeddingService
from src.adapters.embedding.sentence_transformer_embedding_service import (
    SentenceTransformerEmbeddingService,
)


def create_file_system_data_source(path: str) -> FileSystemDataSource:
    if not isinstance(path, str) or not path:
        raise ValueError("FileSystemDataSource requires a non-empty string path.")
    return FileSystemDataSource(path=path)


def create_s3_data_source(bucket: str, prefix: str) -> S3DataSource:
    if not isinstance(bucket, str) or not bucket:
        raise ValueError("S3DataSource requires a non-empty string bucket.")
    if not isinstance(prefix, str):
        raise ValueError("S3DataSource requires a string prefix.")
    return S3DataSource(bucket=bucket, prefix=prefix)


def create_chunking_strategy(
    chunk_size: int, chunk_overlap: int
) -> LangchainChunkingStrategy:
    if not isinstance(chunk_size, int):
        raise ValueError("chunk_size must be an integer.")
    if not isinstance(chunk_overlap, int):
        raise ValueError("chunk_overlap must be an integer.")
    return LangchainChunkingStrategy(chunk_size=chunk_size, chunk_overlap=chunk_overlap)


def create_faiss_vector_repository(
    persist_path: str | dict,
    embedding_service: IEmbeddingService | dict,
    s3_bucket: Optional[str] = None,
    s3_key: Optional[str] = None,
) -> FaissVectorRepository:
    """
    Accepts either a string or a config dict for persist_path for flexibility with config-driven setups.
    Accepts either an embedding service instance or a config dict for embedding_service.
    """
    # If persist_path is a dict (from config), extract the actual path and S3 info
    if isinstance(persist_path, dict):
        path = persist_path.get("path") or persist_path.get("persist_path")
        s3_bucket = persist_path.get("s3_bucket", s3_bucket)
        s3_key = persist_path.get("s3_key", s3_key)
    else:
        path = persist_path

    if not isinstance(path, str) or not path:
        raise ValueError(
            f"FaissVectorRepository requires a non-empty string persist_path. Got: {path!r}"
        )

    # If embedding_service is a dict (from config), create the actual service
    if isinstance(embedding_service, dict):
        embedding_service = create_embedding_service(embedding_service)

    get_dim = getattr(embedding_service, "get_dimension", None)
    if not callable(get_dim):
        # 🟨 CAUTION: Fallback for legacy embedding services missing get_dimension
        # For SentenceTransformerEmbeddingService, try to infer dimension from the model if possible
        if hasattr(embedding_service, "model") and hasattr(
            embedding_service.model, "get_sentence_embedding_dimension"
        ):
            embedding_dim = embedding_service.model.get_sentence_embedding_dimension()
        else:
            raise ValueError(
                f"embedding_service must implement get_dimension(). "
                f"Got type: {type(embedding_service)} with attributes: {dir(embedding_service)}. "
                "If using SentenceTransformerEmbeddingService, ensure it implements get_dimension() "
                "or its model exposes get_sentence_embedding_dimension()."
            )
    else:
        embedding_dim = embedding_service.get_dimension()
    return FaissVectorRepository(
        embedding_dim=embedding_dim,
        persist_path=path,
        s3_bucket=s3_bucket,
        s3_key=s3_key,
    )


# Alias for compatibility with legacy imports and API usage
create_vector_repository = create_faiss_vector_repository


def create_embedding_service(provider: str | dict, **kwargs) -> IEmbeddingService:
    """
    Factory for embedding services. Accepts either a provider string or a config dict.
    """
    if provider is None:
        raise ValueError("Embedding service provider config is required")
    if isinstance(provider, dict):
        provider_type = provider.get("type")
        if provider_type is None:
            raise ValueError(
                "Embedding service provider dict must include a 'type' key"
            )
        config = {**provider}
        config.pop("type", None)
        return create_embedding_service(provider_type, **config)
    if provider == "bedrock":
        return BedrockEmbeddingService(**kwargs)
    elif provider == "sentence_transformer":
        return SentenceTransformerEmbeddingService(**kwargs)
    else:
        raise ValueError(f"Unknown embedding service provider: {provider}")


def create_data_source(source_type: Literal["file_system", "s3"], **kwargs: Any):
    """
    Unified factory for data sources. Use source_type to select implementation.
    Example:
        create_data_source("file_system", path="data/")
        create_data_source("s3", bucket="my-bucket", prefix="my-prefix/")
    """
    if source_type == "file_system":
        return create_file_system_data_source(kwargs["path"])
    elif source_type == "s3":
        return create_s3_data_source(kwargs["bucket"], kwargs["prefix"])
    else:
        raise ValueError(f"Unknown data source type: {source_type}")
