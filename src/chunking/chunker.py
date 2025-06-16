import re
from typing import List, Optional
from chunking.chunking_strategy import get_chunking_pattern

class CodeChunker:
    """
    Splits code or text into semantically meaningful chunks for embedding and retrieval.
    """
    def __init__(self, max_chunk_size: int = 512):
        self.max_chunk_size = max_chunk_size

    def chunk_file(self, file_path: str, language: str = "python", framework: Optional[str] = None) -> List[str]:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return self.chunk_text(content, language=language, framework=framework)

    def chunk_text(self, text: str, language: str = "python", framework: Optional[str] = None) -> List[str]:
        pattern = get_chunking_pattern(language, framework)

        if pattern and re.search(pattern, text, re.MULTILINE):
            raw_chunks = re.split(pattern, text, flags=re.MULTILINE)
            # Re-attach the split tokens
            code_chunks = []
            buffer = ""
            for part in raw_chunks:
                if re.match(pattern, part, re.MULTILINE) and buffer:
                    code_chunks.append(buffer.strip())
                    buffer = part
                else:
                    buffer += part
            if buffer:
                code_chunks.append(buffer.strip())
            return self._split_large_chunks(code_chunks)
        else:
            # Fallback: split on paragraphs
            paragraphs = text.split("\n\n")
            return self._split_large_chunks(paragraphs)

    def _split_large_chunks(self, chunks: List[str]) -> List[str]:
        final_chunks = []
        for chunk in chunks:
            if len(chunk) <= self.max_chunk_size:
                final_chunks.append(chunk)
            else:
                lines = chunk.splitlines()
                buffer = []
                count = 0
                for line in lines:
                    buffer.append(line)
                    count += len(line) + 1
                    if count >= self.max_chunk_size:
                        final_chunks.append("\n".join(buffer))
                        buffer = []
                        count = 0
                if buffer:
                    final_chunks.append("\n".join(buffer))
        return [c for c in final_chunks if c.strip()]