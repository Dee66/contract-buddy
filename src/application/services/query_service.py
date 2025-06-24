import logging
from typing import Any, Dict, List, Optional

from src.domain.entities.chunk import Chunk
from src.domain.ports import IEmbeddingService, IVectorRepository


class QueryService:
    """
    Service for querying the vector store using an embedding service and vector repository.
    """

    def __init__(
        self,
        embedding_service: IEmbeddingService,
        vector_repository: IVectorRepository,
    ):
        self.embedding_service = embedding_service
        self.vector_repository = vector_repository

    def query(
        self, question: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Handles a user query, optionally using additional context.
        Returns a structured response suitable for API or notebook consumption.
        """
        if not self.embedding_service or not self.vector_repository:
            return {"error": "QueryService is not fully configured."}

        # Step 1: Embed the question
        embedding = self.embedding_service.embed_query(question)

        # Step 2: Query the vector store using the correct interface method
        # Use search(), not query(), and pass context as metadata_filter if present
        results = self.vector_repository.search(
            query_embedding=embedding,
            top_k=3,
            metadata_filter=context,
        )

        # Step 3: Format and return the response
        return {
            "question": question,
            "results": [
                {
                    "chunk_id": chunk.id,
                    "content": chunk.content,
                    "score": score,
                    "metadata": chunk.metadata,
                }
                for chunk, score in results
            ],
            "meta": {"service": "QueryService", "version": "1.0.0"},
        }

    def search(self, query: str, top_k: int = 3) -> List[Chunk]:
        """
        Given a query string, returns the top_k most relevant document chunks.
        """
        logging.info("Embedding query text...")
        query_embedding = self.embedding_service.embed_query(query)
        logging.info("Searching vector repository...")
        results = self.vector_repository.search(query_embedding, top_k=top_k)
        # Only return the Chunk objects, not the (Chunk, score) tuples
        return [chunk for chunk, _ in results]
