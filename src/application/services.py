from typing import List
from src.domain.entities import Chunk
from src.domain.ports import (
    IDataSource,
    IChunkingStrategy,
    IEmbeddingService,
    IVectorRepository,
)
import logging


class IngestionService:
    """
    Orchestrates the document ingestion pipeline.
    This service depends on abstractions (ports) defined in the domain layer,
    allowing for flexible implementation of each step.
    """

    def __init__(
        self,
        data_source: IDataSource,
        chunking_strategy: IChunkingStrategy,
        embedding_service: IEmbeddingService,
        vector_repository: IVectorRepository,
    ):
        self.data_source = data_source
        self.chunking_strategy = chunking_strategy
        self.embedding_service = embedding_service
        self.vector_repository = vector_repository
        logging.info("IngestionService initialized.")

    def run(self) -> None:
        """Executes the end-to-end ingestion process."""
        logging.info("Starting ingestion run...")

        # 1. Load documents from the data source
        documents = self.data_source.load()
        if not documents:
            logging.warning("No documents found to ingest.")
            return
        logging.info(f"Loaded {len(documents)} documents.")

        # 2. Process each document
        all_chunks = []
        for doc in documents:
            doc.create_chunks(self.chunking_strategy)
            all_chunks.extend(doc.chunks)

        if not all_chunks:
            logging.error("No chunks were created from the documents.")
            return
        logging.info(f"Created a total of {len(all_chunks)} chunks.")

        # 3. Embed the chunks
        chunk_embeddings = self.embedding_service.embed_chunks(all_chunks)

        for chunk, embedding in zip(all_chunks, chunk_embeddings):
            chunk.metadata["embedding"] = embedding

        logging.info("Successfully generated embeddings for all chunks.")

        # 4. Add chunks to the vector repository
        self.vector_repository.add(all_chunks)
        logging.info("Successfully added all chunks to the vector repository.")
        logging.info("Ingestion run completed.")


class QueryService:
    """
    Orchestrates the document query and retrieval process.
    """

    def __init__(
        self,
        embedding_service: IEmbeddingService,
        vector_repository: IVectorRepository,
    ):
        self.embedding_service = embedding_service
        self.vector_repository = vector_repository
        logging.info("QueryService initialized.")

    def search(self, query: str, top_k: int = 5) -> List[Chunk]:
        """
        Performs a search for a given query.
        1. Embeds the query string into a vector.
        2. Searches the vector repository for the most similar chunks.
        3. Returns the retrieved chunks.
        """
        logging.info(f"Received query: '{query}'")

        # 1. Embed the query
        query_embedding = self.embedding_service.embed_query(query)
        logging.debug("Successfully embedded query string.")

        # 2. Search the vector repository
        retrieved_chunks = self.vector_repository.search(
            query_embedding=query_embedding, top_k=top_k
        )
        logging.info(
            f"Retrieved {len(retrieved_chunks)} chunks from the vector repository."
        )

        return retrieved_chunks
