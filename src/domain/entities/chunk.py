from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import numpy as np


@dataclass
class Chunk:
    """A piece of text split from a Document, ready for vectorization."""

    id: str
    document_id: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[np.ndarray] = field(default=None, repr=False)

    def __post_init__(self):
        # Ensure embedding is a numpy array if provided
        if self.embedding is not None and not isinstance(self.embedding, np.ndarray):
            self.embedding = np.array(self.embedding, dtype=np.float32)
