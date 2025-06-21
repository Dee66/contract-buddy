from dataclasses import dataclass, field
from typing import List, Dict, Any, TYPE_CHECKING
import uuid

from .chunk import Chunk

# Use a TYPE_CHECKING block to import for type hints only.
# This prevents circular import errors at runtime.
if TYPE_CHECKING:
    from src.domain.ports import IChunkingStrategy


@dataclass
class Document:
    """Represents a source document before processing."""

    # Non-default fields must come before default fields.
    source_location: str
    content: str

    # Fields with default values
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: Dict[str, Any] = field(default_factory=dict)
    chunks: List[Chunk] = field(default_factory=list)

    def create_chunks(self, chunking_strategy: "IChunkingStrategy") -> None:
        """
        Creates chunks from the document content using a given strategy.
        This is a core business rule encapsulated within the entity.
        """
        if not self.content:
            return
        self.chunks = chunking_strategy.chunk(self)
