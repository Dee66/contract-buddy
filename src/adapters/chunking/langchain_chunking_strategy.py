from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.domain.ports import IChunkingStrategy
from src.domain.entities import Document, Chunk


class LangchainChunkingStrategy(IChunkingStrategy):
    """
    A concrete implementation of the chunking strategy using Langchain's
    RecursiveCharacterTextSplitter. This is an adapter that connects our
    domain's abstract port to a specific external library.
    """

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )

    def chunk(self, documents: List[Document]) -> List[Chunk]:
        """
        Uses the configured Langchain splitter to chunk the document content.
        """
        all_chunks = []
        for doc in documents:
            split_texts = self._splitter.split_text(doc.content)
            for i, text in enumerate(split_texts):
                chunk_id = f"{doc.id}_chunk_{i}"
                all_chunks.append(
                    Chunk(
                        id=chunk_id,
                        document_id=doc.id,
                        content=text,
                        metadata={"source": doc.metadata.get("source")},
                    )
                )
        return all_chunks
