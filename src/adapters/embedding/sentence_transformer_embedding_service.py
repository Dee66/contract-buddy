import logging
import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer  # type: ignore
from src.domain.ports import IEmbeddingService
from src.domain.entities import Chunk


class SentenceTransformerEmbeddingService(IEmbeddingService):
    """
    An embedding service that uses a local SentenceTransformer model.
    This adapter is ideal for development, testing, or when cloud services
    like Bedrock are unavailable.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        try:
            self.model = SentenceTransformer(model_name)
            logging.info(
                f"Initialized SentenceTransformerEmbeddingService with model: {model_name}"
            )
        except Exception as e:
            logging.error(
                f"Failed to load SentenceTransformer model '{model_name}': {e}"
            )
            raise

    def embed_chunks(self, chunks: List[Chunk]) -> None:
        """
        Generates embeddings for a list of chunks in-place using the local model.
        This implementation processes chunks in a batch for efficiency.
        """
        if not chunks:
            return

        contents = [chunk.content for chunk in chunks if chunk.content]
        if not contents:
            return

        embeddings = self.model.encode(contents, show_progress_bar=False)

        # Assign embeddings back to the corresponding chunks
        chunk_idx = 0
        for i in range(len(chunks)):
            if chunks[i].content:
                chunks[i].embedding = np.array(embeddings[chunk_idx], dtype=np.float32)
                chunk_idx += 1

    def embed_query(self, query: str) -> np.ndarray:
        """
        Generates an embedding for a single query string.
        """
        embedding = self.model.encode(query, show_progress_bar=False)
        return np.array(embedding, dtype=np.float32)

    def get_dimension(self) -> int:
        """
        Returns the dimensionality of the embeddings produced by this service.
        """
        dim = self.model.get_sentence_embedding_dimension()
        # 🟨 CAUTION: Defensive fallback for None (should not occur in production, but ensures type safety)
        if dim is None:
            raise ValueError(
                "SentenceTransformer model did not return a valid embedding dimension."
            )
        return int(dim)
