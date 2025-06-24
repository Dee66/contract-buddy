from abc import ABC, abstractmethod
from typing import List, Dict, Any, TYPE_CHECKING, Tuple, Optional
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
    def chunk(self, document: "Document") -> List["Chunk"]:
        """
        Chunks a single document.

        Args:
            document: The Document entity to be chunked.

        Returns:
            A list of Chunk entities derived from the document.
        """
        pass


class IDataSource(ABC):
    """
    Abstract interface for a data source from which to load documents.
    Implementations will handle connections to sources like file systems, S3, etc.
    """

    @abstractmethod
    def get_all_source_document_identifiers(self) -> List[str]:
        """
        Retrieves a list of unique identifiers for all documents currently in the source.
        This is used to reconcile deletions.
        """
        pass

    @abstractmethod
    def load_all(self) -> List["Document"]:
        """Loads all documents from the source, regardless of history."""
        pass

    @abstractmethod
    def load_new(self, last_known_ids: List[str]) -> List["Document"]:
        """
        Loads only documents that are new or have changed since the last run.

        Args:
            last_known_ids: A list of unique identifiers (e.g., file paths or S3 ETags)
                            of documents that have already been processed.

        Returns:
            A list of new or updated documents.
        """
        pass

    @abstractmethod
    def load(self, doc_id: str) -> "Document":
        """
        Loads a single document by its unique identifier.
        Returns the Document if found, or raises an exception if not found.
        """
        pass


class IVectorRepository(ABC):
    """
    Abstract interface for a repository that stores and retrieves vectorized chunks.
    This is the primary port for interacting with our vector database adapter.
    """

    @abstractmethod
    def get_all_document_identifiers(self) -> List[str]:
        """Retrieves the unique identifiers of all documents currently in the store."""
        pass

    @abstractmethod
    def delete_by_document_id(self, doc_ids: List[str]) -> None:
        """Removes all chunks associated with the given document IDs."""
        pass

    @abstractmethod
    def add(self, chunks: List["Chunk"]) -> None:
        """Adds a list of chunks to the vector store."""
        pass

    @abstractmethod
    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[Tuple["Chunk", float]]:
        """
        Searches for chunks similar to a query embedding.
        Returns a list of tuples, where each tuple contains the retrieved chunk
        and its similarity score (distance).
        """
        pass

    @abstractmethod
    def save(self) -> None:
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

    @abstractmethod
    def get_dimension(self) -> int:
        """
        Returns the dimensionality of the embeddings produced by this service.
        This is required for initializing vector repositories (e.g., FAISS).
        """
        pass
