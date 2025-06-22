import faiss
import numpy as np
import logging
import boto3
import json
import threading
from botocore.exceptions import ClientError
from pathlib import Path
from typing import List, Tuple
from src.domain.entities.chunk import Chunk
from src.domain.ports import IVectorRepository


class FaissVectorRepository(IVectorRepository):
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
        self.metadata_path = self.persist_path.with_suffix(".meta.json")
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.s3_metadata_key = (
            f"{s3_key.rsplit('.', 1)[0]}.meta.json" if s3_key else None
        )
        self.index = None
        self.chunks: List[Chunk] = []
        self.s3_client = boto3.client("s3")
        self.last_known_s3_version_id = None
        self.reload_lock = threading.Lock()
        self._load()

    def _load(self):
        """
        Orchestrates loading the index and metadata atomically.
        It loads into temporary variables and only replaces the instance
        attributes upon a fully successful load.
        """
        temp_index = None
        temp_chunks = None

        # Step 1: Attempt to load from S3 to local disk
        self._load_from_s3()

        # Step 2: Attempt to load from local disk into memory
        if self.persist_path.exists() and self.metadata_path.exists():
            try:
                logging.info(f"Loading FAISS index from {self.persist_path}")
                temp_index = faiss.read_index(str(self.persist_path))

                logging.info(f"Loading chunk metadata from {self.metadata_path}")
                with open(self.metadata_path, "r") as f:
                    chunks_data = json.load(f)
                    temp_chunks = [Chunk.model_validate(c) for c in chunks_data]

                if temp_index.ntotal != len(temp_chunks):
                    logging.warning(
                        "Loaded index and metadata have a size mismatch. Load aborted."
                    )
                    return  # Abort the load, keep the old index active

                # --- Atomic Swap ---
                # If we reached here, loading was successful.
                # Now, we atomically update the instance variables.
                self.index = temp_index
                self.chunks = temp_chunks
                logging.info(
                    f"Successfully loaded and swapped to new index with {self.index.ntotal} vectors."
                )

            except Exception as e:
                logging.error(
                    f"Failed to load index or metadata from disk: {e}. The old index remains active."
                )
                return  # Abort the load

        # Step 3: If no index exists after attempting load, initialize a new one.
        if self.index is None:
            logging.warning("No existing index found. Initializing a new FAISS index.")
            self.index = faiss.IndexFlatL2(self.embedding_dim)
            self.chunks = []

    def _load_from_s3(self):
        if not self.s3_bucket or not self.s3_key:
            return
        # Use the class-level S3 client for consistency
        s3 = self.s3_client
        # Download index file
        try:
            logging.info(
                f"Attempting to download index from s3://{self.s3_bucket}/{self.s3_key}"
            )
            self.persist_path.parent.mkdir(parents=True, exist_ok=True)
            s3.download_file(self.s3_bucket, self.s3_key, str(self.persist_path))
        except ClientError as e:
            if e.response["Error"]["Code"] != "404":
                raise
        # Download metadata file
        try:
            logging.info(
                f"Attempting to download metadata from s3://{self.s3_bucket}/{self.s3_metadata_key}"
            )
            response = self.s3_client.get_object(
                Bucket=self.s3_bucket, Key=self.s3_metadata_key
            )
            with open(self.metadata_path, "wb") as f:
                f.write(response["Body"].read())
            # Store the version ID to detect changes
            self.last_known_s3_version_id = response.get("VersionId")
            logging.info(
                f"Successfully downloaded metadata version: {self.last_known_s3_version_id}"
            )
        except ClientError as e:
            if e.response["Error"]["Code"] != "404":
                raise

    def _load_from_disk(self):
        """This method is now deprecated in favor of the atomic _load()."""
        pass

    def get_all_document_identifiers(self) -> List[str]:
        if not self.chunks:
            return []
        return list({chunk.document_id for chunk in self.chunks})

    def delete_by_document_id(self, doc_ids_to_delete: List[str]):
        """
        Removes all chunks associated with the given document IDs by rebuilding the index.
        This is the safest method for FAISS to ensure consistency.
        """
        if not doc_ids_to_delete:
            return

        initial_chunk_count = len(self.chunks)

        # Identify chunks and their original indices to keep
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

        # Create a new index and add only the vectors we want to keep
        new_index = faiss.IndexFlatL2(self.embedding_dim)
        if chunks_to_keep:
            vectors_to_keep = np.array(
                [chunk.embedding for chunk in chunks_to_keep]
            ).astype("float32")
            new_index.add(vectors_to_keep)

        # Atomically replace the old index and chunk list
        self.index = new_index
        self.chunks = chunks_to_keep
        logging.info(f"Index rebuilt. New size: {self.index.ntotal} vectors.")

    def _check_for_updates_and_reload(self):
        """
        Checks S3 for a new version of the metadata and reloads if found.
        This operation is protected by a lock to ensure thread safety.
        """
        if not self.s3_bucket or not self.s3_metadata_key:
            return

        # Acquire lock to prevent race conditions from multiple API workers
        with self.reload_lock:
            try:
                response = self.s3_client.head_object(
                    Bucket=self.s3_bucket, Key=self.s3_metadata_key
                )
                latest_version_id = response.get("VersionId")

                if (
                    latest_version_id
                    and latest_version_id != self.last_known_s3_version_id
                ):
                    logging.info(
                        f"New index version detected. Old: {self.last_known_s3_version_id}, New: {latest_version_id}. Reloading..."
                    )
                    self._load()  # Trigger a full reload from S3 and disk

            except ClientError as e:
                if e.response["Error"]["Code"] == "404":
                    if self.last_known_s3_version_id is not None:
                        logging.warning(
                            "Index appears to have been deleted from S3. Clearing local state."
                        )
                        self.index = faiss.IndexFlatL2(self.embedding_dim)
                        self.chunks = []
                        self.last_known_s3_version_id = None
                else:
                    logging.error(f"Error checking for index updates in S3: {e}")

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
        self, query_embedding: np.ndarray, top_k: int, metadata_filter: dict = None
    ) -> List[Tuple[Chunk, float]]:
        # This is the hot-reload trigger point.
        self._check_for_updates_and_reload()

        if self.index.ntotal == 0:
            return []

        # FAISS doesn't support pre-filtering. We fetch more results (k*4 or 100)
        # and filter them in memory. This is a common pattern for FAISS.
        k_for_search = max(top_k * 4, 100) if metadata_filter else top_k

        # Ensure the input is a 2D numpy array for FAISS
        if query_embedding.ndim == 1:
            query_embedding = np.expand_dims(query_embedding, axis=0)

        distances, indices = self.index.search(
            query_embedding.astype("float32"), k_for_search
        )

        results = []
        for i, dist in zip(indices[0], distances[0]):
            if i == -1:
                continue

            chunk = self.chunks[i]

            # Apply metadata filter if provided
            if metadata_filter:
                match = all(
                    chunk.metadata.get(key) == value
                    for key, value in metadata_filter.items()
                )
                if not match:
                    continue

            results.append((chunk, float(dist)))

            # Stop once we have enough results that match the filter
            if len(results) >= top_k:
                break

        return results

    def save(self):
        """Saves the FAISS index and chunk metadata to disk and uploads to S3."""
        if self.index is None or self.index.ntotal == 0:
            logging.info("Index is empty. Nothing to save.")
            return

        self.persist_path.parent.mkdir(parents=True, exist_ok=True)

        logging.info(f"Saving FAISS index to {self.persist_path}")
        faiss.write_index(self.index, str(self.persist_path))

        logging.info(f"Saving chunk metadata to {self.metadata_path}")
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

            # After a successful save, update the known version ID immediately
            response = s3.head_object(Bucket=self.s3_bucket, Key=self.s3_metadata_key)
            self.last_known_s3_version_id = response.get("VersionId")
            logging.info(
                f"Successfully uploaded index and metadata to S3. New version: {self.last_known_s3_version_id}"
            )
        except ClientError as e:
            logging.error(f"Failed to upload index or metadata to S3: {e}")
            raise
