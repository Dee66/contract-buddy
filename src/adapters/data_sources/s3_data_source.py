import boto3
import logging
from typing import List
from botocore.exceptions import ClientError
from src.domain.entities.document import Document
from src.domain.ports import IDataSource


class S3DataSource(IDataSource):
    """A data source that reads documents from an AWS S3 bucket."""

    def __init__(self, bucket: str, prefix: str):
        self.bucket = bucket
        self.prefix = prefix
        self.s3_client = boto3.client("s3")
        logging.info(
            f"Initialized S3DataSource for bucket '{bucket}' and prefix '{prefix}'"
        )

    def _list_objects(self) -> List[dict]:
        """Helper to list all objects under the configured prefix."""
        try:
            paginator = self.s3_client.get_paginator("list_objects_v2")
            pages = paginator.paginate(Bucket=self.bucket, Prefix=self.prefix)
            return [obj for page in pages for obj in page.get("Contents", [])]
        except ClientError as e:
            logging.error(
                f"Error listing objects in s3://{self.bucket}/{self.prefix}: {e}"
            )
            return []

    def _load_document_from_s3(self, s3_object: dict) -> Document:
        """Loads a single document's content from S3."""
        key = s3_object["Key"]
        try:
            response = self.s3_client.get_object(Bucket=self.bucket, Key=key)
            content = response["Body"].read().decode("utf-8")
            # The ETag is a unique identifier for the object's version.
            # It's the perfect ID for checking if a file has changed.
            doc_id = s3_object["ETag"].strip('"')
            return Document(
                id=doc_id,
                content=content,
                metadata={"source": f"s3://{self.bucket}/{key}"},
            )
        except ClientError as e:
            logging.error(f"Error reading object s3://{self.bucket}/{key}: {e}")
            return None
        except Exception as e:
            logging.error(
                f"Failed to decode or process object s3://{self.bucket}/{key}: {e}"
            )
            return None

    def get_all_source_document_identifiers(self) -> List[str]:
        """Retrieves all document ETags from the S3 source."""
        logging.info("Fetching all document identifiers from source...")
        s3_objects = self._list_objects()
        # The ETag is our canonical document ID for S3 objects
        return [obj.get("ETag", "").strip('"') for obj in s3_objects if obj.get("ETag")]

    def load_all(self) -> List[Document]:
        """Loads all documents from the S3 source."""
        logging.info("Executing full load from S3...")
        s3_objects = self._list_objects()
        documents = [self._load_document_from_s3(obj) for obj in s3_objects if obj]
        return [doc for doc in documents if doc]

    def load_new(self, last_known_ids: List[str]) -> List[Document]:
        """Loads only new or modified documents from S3 by comparing ETags."""
        logging.info("Executing incremental load from S3...")
        s3_objects = self._list_objects()

        new_or_modified_objects = [
            obj
            for obj in s3_objects
            if obj.get("ETag", "").strip('"') not in last_known_ids
        ]

        if not new_or_modified_objects:
            logging.info("No new or modified S3 objects found.")
            return []

        logging.info(
            f"Found {len(new_or_modified_objects)} new or modified S3 objects to process."
        )
        documents = [
            self._load_document_from_s3(obj) for obj in new_or_modified_objects if obj
        ]
        return [doc for doc in documents if doc]
