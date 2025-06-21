from abc import ABC, abstractmethod
from typing import List, Dict, Any, TYPE_CHECKING
import numpy as np

# Use a TYPE_CHECKING block to import for type hints only.
# This prevents circular import errors at runtime.
if TYPE_CHECKING:
    from src.domain.entities import Document, Chunk


class IChunkingStrategy(ABC):
    """
    Abstract interface for a document chunking strategy.
    Implementations will define how a single document is split into chunks.
    """

    @abstractmethod
    def chunk(self, documents: List["Document"]) -> List["Chunk"]:
        pass


class IDataSource(ABC):
    """
    Abstract interface for a data source from which to load documents.
    Implementations will handle connections to sources like file systems, S3, etc.
    """

    @abstractmethod
    def load(self) -> List["Document"]:
        pass


class IVectorRepository(ABC):
    """
    Abstract interface for a repository that stores and retrieves vectorized chunks.
    This is the primary port for interacting with our vector database adapter.
    """

    @abstractmethod
    def add(self, chunks: List["Chunk"]) -> None:
        """Adds a list of chunks to the vector store."""
        pass

    @abstractmethod
    def search(
        self, query_embedding: np.ndarray, top_k: int, metadata_filter: Dict[str, Any]
    ) -> List["Chunk"]:
        """Searches for chunks similar to a query embedding."""
        pass

    @abstractmethod
    def persist(self) -> None:
        """
        Persists the current state of the index to storage.
        This is crucial for file-based vector stores like FAISS.
        """
        pass


class IEmbeddingService(ABC):
    """
    Abstract interface for a service that generates vector embeddings.
    This abstracts the specific model (e.g., Bedrock, SentenceTransformers).
    """

    @abstractmethod
    def embed_chunks(self, chunks: List["Chunk"]) -> None:
        """
        Generates embeddings and assigns them to the .embedding attribute
        of each chunk object in the list, modifying them in-place.
        """
        pass

    @abstractmethod
    def embed_query(self, query: str) -> np.ndarray:
        """Generates an embedding for a single query string."""
        pass
