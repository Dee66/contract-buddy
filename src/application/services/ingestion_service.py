import logging
from typing import List
from src.domain.ports import (
    IDataSource,
    IChunkingStrategy,
    IEmbeddingService,
    IVectorRepository,
)
from src.domain.entities.document import Document
from src.domain.entities.chunk import Chunk


class IngestionService:
    """
    This service orchestrates the data ingestion pipeline.
    It represents a single, complete use case in the application.
    """

    def __init__(
        self,
        data_source: IDataSource,
        chunking_strategy: IChunkingStrategy,
        embedding_service: IEmbeddingService,
        vector_repository: IVectorRepository,
    ):
        """
        Initializes the service with its dependencies, injected via interfaces (Ports).
        This adheres to the Dependency Inversion Principle.
        """
        self.data_source = data_source
        self.chunking_strategy = chunking_strategy
        self.embedding_service = embedding_service
        self.vector_repository = vector_repository
        logging.info("IngestionService initialized with all dependencies.")

    def ingest(self) -> None:
        """
        Executes the full ingestion pipeline:
        1. Loads documents from the data source.
        2. Splits documents into chunks.
        3. Generates vector embeddings for each chunk.
        4. Adds the vectorized chunks to the repository.
        5. Persists the repository state.
        """
        logging.info("Starting document ingestion process...")

        # 1. Load all documents
        documents: List[Document] = self.data_source.load_all()
        if not documents:
            logging.warning("No documents found to ingest. Pipeline finished early.")
            return
        logging.info(f"Loaded {len(documents)} documents.")

        # 2. Chunk
        all_chunks: List[Chunk] = []
        for doc in documents:
            chunks = self.chunking_strategy.chunk(doc)
            all_chunks.extend(chunks)
        logging.info(f"Split documents into {len(all_chunks)} chunks.")

        # 3. Embed
        self.embedding_service.embed_chunks(all_chunks)
        logging.info("Generated embeddings for all chunks.")

        # 4. Add to repository
        self.vector_repository.add(all_chunks)
        logging.info("Added chunks to the vector repository.")

        # 5. Persist
        self.vector_repository.save()
        logging.info("Persisted the vector repository.")

        logging.info("Document ingestion process completed successfully.")
