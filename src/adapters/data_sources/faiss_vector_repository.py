import faiss
import numpy as np
import logging
import boto3
import json
from botocore.exceptions import ClientError
from pathlib import Path
from typing import List, Tuple
from src.domain.entities.chunk import Chunk
from src.domain.ports import VectorRepository


class FaissVectorRepository(VectorRepository):
    """A vector repository using FAISS that can persist to S3."""

    def __init__(
        self,
        embedding_dim: int,
        persist_path: str,
        s3_bucket: str = None,
        s3_key: str = None,
    ):
        self.embedding_dim = embedding_dim
        self.persist_path = Path(persist_path)
        self.metadata_path = self.persist_path.with_suffix(".json")
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.s3_metadata_key = f"{s3_key}.json" if s3_key else None
        self.index = None
        self.chunks: List[Chunk] = []
        self._load_from_s3()
        self._load_from_disk()

    def _load_from_s3(self):
        if not self.s3_bucket or not self.s3_key:
            return

        s3 = boto3.client("s3")
        self.persist_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            logging.info(
                f"Attempting to download index from s3://{self.s3_bucket}/{self.s3_key}"
            )
            s3.download_file(self.s3_bucket, self.s3_key, str(self.persist_path))
            logging.info("Successfully downloaded index from S3.")

            logging.info(
                f"Attempting to download metadata from s3://{self.s3_bucket}/{self.s3_metadata_key}"
            )
            s3.download_file(
                self.s3_bucket, self.s3_metadata_key, str(self.metadata_path)
            )
            logging.info("Successfully downloaded metadata from S3.")

        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                logging.warning(
                    "Index or metadata not found in S3. A new one will be created."
                )
            else:
                logging.error(f"Error downloading from S3: {e}")
                raise

    def _load_from_disk(self):
        if self.persist_path.exists() and self.metadata_path.exists():
            try:
                logging.info(f"Loading FAISS index from {self.persist_path}")
                self.index = faiss.read_index(str(self.persist_path))

                logging.info(f"Loading metadata from {self.metadata_path}")
                with open(self.metadata_path, "r") as f:
                    chunks_data = json.load(f)
                    self.chunks = [Chunk.model_validate(c) for c in chunks_data]

                logging.info(
                    f"FAISS index and metadata loaded with {self.index.ntotal} vectors."
                )
            except Exception as e:
                logging.error(f"Failed to load index or metadata from disk: {e}")
                self.index = None
                self.chunks = []

        if self.index is None:
            logging.warning("No existing index found. Initializing a new FAISS index.")
            self.index = faiss.IndexFlatL2(self.embedding_dim)
            self.chunks = []

    def add(self, chunks: List[Chunk]):
        if not chunks:
            return
        vectors = np.array([chunk.embedding for chunk in chunks]).astype("float32")
        self.index.add(vectors)
        self.chunks.extend(chunks)
        logging.info(
            f"Added {len(chunks)} vectors. Index now has {self.index.ntotal} total vectors."
        )

    def search(
        self, query_embedding: List[float], top_k: int
    ) -> List[Tuple[Chunk, float]]:
        if self.index.ntotal == 0:
            return []
        query_vector = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for i, dist in zip(indices[0], distances[0]):
            if i != -1 and i < len(self.chunks):
                results.append((self.chunks[i], float(dist)))
        return results

    def save(self):
        if self.index.ntotal == 0:
            logging.warning("Index is empty. Nothing to save.")
            return

        logging.info(f"Saving FAISS index to {self.persist_path}")
        self.persist_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(self.persist_path))

        logging.info(f"Saving metadata to {self.metadata_path}")
        with open(self.metadata_path, "w") as f:
            chunks_data = [chunk.model_dump() for chunk in self.chunks]
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

            logging.info("Successfully uploaded index and metadata to S3.")
        except ClientError as e:
            logging.error(f"Failed to upload to S3: {e}")
            raise
