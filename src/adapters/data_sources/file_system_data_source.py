import os
import logging
from typing import List
from src.domain.entities.document import Document
from src.domain.ports import IDataSource


class FileSystemDataSource(IDataSource):
    """
    Loads documents from a local file system directory.
    This adapter is suitable for development and processing local data.
    """

    def __init__(self, path: str):
        self.path = path
        logging.info(f"Initialized FileSystemDataSource for path '{path}'")

    def get_all_source_document_identifiers(self) -> List[str]:
        """Returns a list of file names in the directory as document identifiers."""
        try:
            return [
                f
                for f in os.listdir(self.path)
                if os.path.isfile(os.path.join(self.path, f))
            ]
        except Exception as e:
            logging.error(f"Error listing files in {self.path}: {e}")
            return []

    def load_all(self) -> List[Document]:
        """Loads all documents from the file system."""
        doc_ids = self.get_all_source_document_identifiers()
        return [self.load(doc_id) for doc_id in doc_ids]

    def load_new(self, last_known_ids: List[str]) -> List[Document]:
        """Loads only new or modified documents by comparing file names."""
        current_ids = set(self.get_all_source_document_identifiers())
        new_ids = current_ids - set(last_known_ids)
        return [self.load(doc_id) for doc_id in new_ids]

    def load(self, doc_id: str) -> Document:
        """Loads a single document by its file name."""
        file_path = os.path.join(self.path, doc_id)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return Document(
                id=doc_id,
                content=content,
                source_location=file_path,
                metadata={"source": file_path},
            )
        except Exception as e:
            logging.error(f"Error loading file {file_path}: {e}")
            raise
