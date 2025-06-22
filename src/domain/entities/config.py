from pydantic import BaseModel, Field

# --- Individual Component Models ---


class DataSourceConfig(BaseModel):
    type: str
    path: str | None = None  # Used by file_system
    bucket: str | None = None  # Used by s3
    prefix: str | None = None  # Used by s3


class ChunkingStrategyConfig(BaseModel):
    type: str
    chunk_size: int = Field(..., gt=0)
    chunk_overlap: int = Field(..., ge=0)


class EmbeddingServiceConfig(BaseModel):
    type: str
    model_name: str | None = None
    aws_region: str | None = None
    model_id: str | None = None


class VectorRepositoryConfig(BaseModel):
    type: str
    persist_path: str  # Local path inside the container
    s3_bucket: str | None = None  # Used for cloud persistence
    s3_key: str | None = None  # Used for cloud persistence


# --- Top-Level Application Configuration Model ---


class AppConfig(BaseModel):
    """The main configuration model that holds all component configurations."""

    data_source: DataSourceConfig
    chunking_strategy: ChunkingStrategyConfig
    embedding_service: EmbeddingServiceConfig
    vector_repository: VectorRepositoryConfig
