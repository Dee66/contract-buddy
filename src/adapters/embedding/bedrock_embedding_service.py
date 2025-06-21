import boto3
import json
import logging
import numpy as np
from typing import List

from src.domain.entities import Chunk
from src.domain.ports import IEmbeddingService


class BedrockEmbeddingService(IEmbeddingService):
    """
    An embedding service that uses AWS Bedrock to generate vector embeddings.
    This is the primary, production-grade implementation.
    """

    def __init__(self, aws_region: str, model_id: str = "amazon.titan-embed-text-v1"):
        self.model_id = model_id
        self.bedrock_runtime = boto3.client(
            service_name="bedrock-runtime", region_name=aws_region
        )
        logging.info(
            f"Initialized BedrockEmbeddingService with model: {self.model_id} in region: {aws_region}"
        )

    def embed_chunks(self, chunks: List[Chunk]) -> None:
        """
        Generates embeddings for a list of chunks in-place using AWS Bedrock.
        """
        for chunk in chunks:
            if chunk.content:
                chunk.embedding = self._get_embedding(chunk.content)

    def embed_query(self, query: str) -> np.ndarray:
        """
        Generates an embedding for a single query string.
        """
        return self._get_embedding(query)

    def _get_embedding(self, text: str) -> np.ndarray:
        """Invokes the Bedrock model to get an embedding for a single text."""
        body = json.dumps({"inputText": text})
        try:
            response = self.bedrock_runtime.invoke_model(
                body=body,
                modelId=self.model_id,
                accept="application/json",
                contentType="application/json",
            )
            response_body = json.loads(response.get("body").read())
            return np.array(response_body.get("embedding"), dtype=np.float32)
        except Exception as e:
            logging.error(f"Bedrock embedding failed for model {self.model_id}: {e}")
            return None
