from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.domain.ports import IChunkingStrategy
from src.domain.entities import Document, Chunk


class LangchainChunkingStrategy(IChunkingStrategy):
    """
    Adapter for LangChain's RecursiveCharacterTextSplitter, implementing our domain's chunking port.
    Ensures Clean Architecture compliance and production-grade chunking for a single Document.
    """

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )

    def chunk(self, document: Document) -> List[Chunk]:
        """
        Splits a single Document into Chunks using LangChain's splitter.
        This signature matches the IChunkingStrategy port (document: Document) -> List[Chunk].
        """
        split_texts = self._splitter.split_text(document.content)
        return [
            Chunk(
                id=f"{document.id}_chunk_{i}",
                document_id=document.id,
                content=text,
                metadata={"source": document.metadata.get("source")},
            )
            for i, text in enumerate(split_texts)
        ]
