import os
import logging
from typing import List
from src.domain.ports import IDataSource
from src.domain.entities import Document


class FileSystemDataSource(IDataSource):
    """
    Loads documents from a local file system directory.
    This adapter is suitable for development and processing local data.
    """

    def __init__(self, path: str):
        if not os.path.isdir(path):
            raise ValueError(f"Path is not a valid directory: {path}")
        self.path = path
        logging.info(f"Initialized FileSystemDataSource with path: {self.path}")

    def load(self) -> List[Document]:
        """
        Loads all .txt files from the configured directory.
        Each file is treated as a separate Document.
        """
        documents = []
        for filename in os.listdir(self.path):
            if filename.endswith(".txt"):
                file_path = os.path.join(self.path, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    doc_id = os.path.splitext(filename)[0]
                    documents.append(
                        Document(
                            id=doc_id, content=content, metadata={"source": file_path}
                        )
                    )
                except Exception as e:
                    logging.error(f"Failed to read or process file {file_path}: {e}")
        logging.info(f"Loaded {len(documents)} documents from {self.path}")
        return documents
