from typing import List, Tuple
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
        """
        Executes a full, idempotent synchronization of the vector store.
        1. Fetches all document IDs from the source and the vector store.
        2. Calculates which documents to add (new/updated) and which to delete.
        3. Executes deletions and additions.
        """
        logging.info("Starting full synchronization run...")

        # 1. Get the current state from the source and the destination (vector store)
        source_doc_ids = set(self.data_source.get_all_source_document_identifiers())
        repo_doc_ids = set(self.vector_repository.get_all_document_identifiers())
        logging.info(
            f"Found {len(source_doc_ids)} documents in source, {len(repo_doc_ids)} in repository."
        )

        # 2. Calculate documents to delete from the repository
        doc_ids_to_delete = list(repo_doc_ids - source_doc_ids)
        if doc_ids_to_delete:
            logging.info(f"Identified {len(doc_ids_to_delete)} documents to delete.")
            self.vector_repository.delete_by_document_id(doc_ids_to_delete)

        # 3. Load only new or updated documents from the data source
        # The S3 adapter uses ETags as IDs, so this correctly identifies new/modified files.
        documents_to_add = self.data_source.load_new(list(repo_doc_ids))
        if not documents_to_add:
            logging.info("No new or updated documents to ingest.")
            self.vector_repository.save()  # Still save to persist deletions
            logging.info("Synchronization run completed.")
            return
        logging.info(
            f"Loaded {len(documents_to_add)} new or updated documents to process."
        )

        # 4. Process and embed new documents
        all_new_chunks = []
        for doc in documents_to_add:
            doc.create_chunks(self.chunking_strategy)
            all_new_chunks.extend(doc.chunks)

        if not all_new_chunks:
            logging.error("No chunks were created from the new documents.")
            return

        self.embedding_service.embed_chunks(all_new_chunks)
        logging.info(
            f"Successfully generated embeddings for {len(all_new_chunks)} new chunks."
        )

        # 5. Add new chunks to the vector repository and persist the final state
        self.vector_repository.add(all_new_chunks)
        self.vector_repository.save()

        logging.info("Successfully added new chunks and saved final state.")
        logging.info("Full synchronization run completed.")


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

    def search(
        self, query: str, top_k: int = 5, metadata_filter: dict = None
    ) -> List[Tuple[Chunk, float]]:
        """
        Performs a search for a given query.
        1. Embeds the query string into a vector.
        2. Searches the vector repository for the most similar chunks.
        3. Returns the retrieved chunks and their similarity scores.
        """
        logging.info(f"Received query: '{query}'")

        # 1. Embed the query
        query_embedding = self.embedding_service.embed_query(query)
        logging.debug("Successfully embedded query string.")

        # 2. Search the vector repository
        retrieved_results = self.vector_repository.search(
            query_embedding=query_embedding,
            top_k=top_k,
            metadata_filter=metadata_filter,
        )
        logging.info(
            f"Retrieved {len(retrieved_results)} results from the vector repository."
        )

        return retrieved_results
