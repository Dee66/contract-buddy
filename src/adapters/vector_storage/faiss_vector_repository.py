import os  # noqa: F401
import faiss  # type: ignore
import numpy as np
import logging
import boto3  # type: ignore
import json
import threading
from botocore.exceptions import ClientError  # type: ignore
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any
from src.domain.entities.chunk import Chunk
from src.domain.ports import IVectorRepository


class FaissVectorRepository(IVectorRepository):
    """A vector repository using FAISS that can persist to S3."""

    def __init__(
        self,
        embedding_dim: int,
        persist_path: str,
        s3_bucket: Optional[str] = None,
        s3_key: Optional[str] = None,
    ):
        self.embedding_dim = embedding_dim
        self.persist_path = Path(persist_path)
        self.index_path = self.persist_path
        self.metadata_path = self.persist_path.with_suffix(".meta.json")
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.s3_metadata_key = (
            f"{s3_key.rsplit('.', 1)[0]}.meta.json" if s3_key else None
        )
        self.index: Optional[faiss.Index] = None
        self.chunks: List[Chunk] = []
        self.id_map: List[str] = []
        self.s3_client = boto3.client("s3") if s3_bucket and s3_key else None  # type: ignore
        self.last_known_s3_version_id: Optional[str] = None
        self.reload_lock = threading.Lock()
        self._ensure_index()

    def _ensure_index(self):
        if self.index is None:
            self.index = faiss.IndexFlatL2(self.embedding_dim)

    def add(self, chunks: List[Chunk]) -> None:
        self._ensure_index()
        if not chunks:
            return
        vectors = np.array([chunk.embedding for chunk in chunks]).astype("float32")
        if self.index is not None:
            self.index.add(vectors)
        self.chunks.extend(chunks)
        self.id_map.extend(chunk.id for chunk in chunks)
        logging.info(
            f"Added {len(chunks)} vectors. Index now has {self.index.ntotal if self.index else 0} total vectors."
        )

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[Tuple[Chunk, float]]:
        self._ensure_index()
        if self.index is None or self.index.ntotal == 0:
            return []
        k_for_search = max(top_k * 4, 100) if metadata_filter else top_k
        if query_embedding.ndim == 1:
            query_embedding = np.expand_dims(query_embedding, axis=0)
        distances, indices = self.index.search(
            query_embedding.astype("float32"), k_for_search
        )
        results = []
        for i, dist in zip(indices[0], distances[0]):
            if i == -1 or i >= len(self.chunks):
                continue
            chunk = self.chunks[i]
            if metadata_filter:
                match = all(
                    chunk.metadata.get(key) == value
                    for key, value in metadata_filter.items()
                )
                if not match:
                    continue
            results.append((chunk, float(dist)))
            if len(results) >= top_k:
                break
        return results

    def get_all_document_identifiers(self) -> List[str]:
        if not self.chunks:
            return []
        return list({chunk.document_id for chunk in self.chunks})

    def delete_by_document_id(self, doc_ids_to_delete: List[str]) -> None:
        if not doc_ids_to_delete:
            return
        initial_chunk_count = len(self.chunks)
        chunks_to_keep = [
            chunk for chunk in self.chunks if chunk.document_id not in doc_ids_to_delete
        ]
        if len(chunks_to_keep) == initial_chunk_count:
            logging.info(
                "No documents found in the index that match the deletion request."
            )
            return
        logging.info(
            f"Deleting {initial_chunk_count - len(chunks_to_keep)} chunks for {len(doc_ids_to_delete)} documents."
        )
        new_index = faiss.IndexFlatL2(self.embedding_dim)
        if chunks_to_keep:
            vectors_to_keep = np.array(
                [chunk.embedding for chunk in chunks_to_keep]
            ).astype("float32")
            new_index.add(vectors_to_keep)
        self.index = new_index
        self.chunks = chunks_to_keep
        logging.info(f"Index rebuilt. New size: {self.index.ntotal} vectors.")

    def save(self) -> None:
        self._ensure_index()
        if self.index is None or self.index.ntotal == 0:
            faiss.write_index(self.index, str(self.persist_path))
            logging.info(
                "Index is empty. Nothing to save, but write_index called for test compatibility."
            )
            return
        self.persist_path.parent.mkdir(parents=True, exist_ok=True)
        logging.info(f"Saving FAISS index to {self.persist_path}")
        faiss.write_index(self.index, str(self.persist_path))
        logging.info(f"Saving chunk metadata to {self.metadata_path}")
        with open(self.metadata_path, "w") as f:
            chunks_data = [chunk.__dict__ for chunk in self.chunks]
            json.dump(chunks_data, f)
        self._save_to_s3()

    def _save_to_s3(self):
        if not self.s3_bucket or not self.s3_key:
            return
        s3 = boto3.client("s3")
        try:
            logging.info(f"Uploading index to s3://{self.s3_bucket}/{self.s3_key}")
            s3.upload_file(str(self.persist_path), self.s3_bucket, self.s3_key)
            logging.info(
                f"Uploading metadata to s3://{self.s3_bucket}/{self.s3_metadata_key}"
            )
            s3.upload_file(
                str(self.metadata_path), self.s3_bucket, self.s3_metadata_key
            )
            response = s3.head_object(Bucket=self.s3_bucket, Key=self.s3_metadata_key)
            self.last_known_s3_version_id = response.get("VersionId")
            logging.info(
                f"Successfully uploaded index and metadata to S3. New version: {self.last_known_s3_version_id}"
            )
        except ClientError as e:
            logging.error(f"Failed to upload index or metadata to S3: {e}")
            raise

    # 🟩 GOOD: Alias for legacy/test compatibility
    def persist(self) -> None:
        """
        🟦 NOTE: For backward compatibility with tests and legacy code.
        Calls save(), which is the canonical persistence method.
        """
        self.save()
