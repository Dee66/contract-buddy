import re
from typing import List, Optional
from src.chunking.chunking_strategy import get_chunking_pattern
from bs4 import BeautifulSoup
import json

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

    def chunk(self, text):
        """
        Splits the input text into chunks of up to max_chunk_size characters.
        Returns a list of chunk strings.
        """
        if not text:
            return []
        return [text[i:i+self.max_chunk_size] for i in range(0, len(text), self.max_chunk_size)]

def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    # Get all visible text (customize as needed)
    text = soup.get_text(separator="\n")
    return text

def chunk_text(text, max_length=300):
    # Split by paragraphs, then by length
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    chunks = []
    for para in paragraphs:
        while len(para) > max_length:
            split_point = para.rfind(' ', 0, max_length)
            if split_point == -1:
                split_point = max_length
            chunks.append(para[:split_point])
            para = para[split_point:].strip()
        if para:
            chunks.append(para)
    return chunks

def process_html_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    text = extract_text_from_html(html_content)
    chunks = chunk_text(text)
    docs = [{"content": chunk} for chunk in chunks if chunk]
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=2)
    print(f"Saved {len(docs)} chunks to {output_path}")

if __name__ == "__main__":
    # Example usage:
    input_html = "data/raw/python_doc.html"  # Path to HTML file
    output_json = "data/clean/docs.json"
    process_html_file(input_html, output_json)