import os
import sys
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

# Ensure the src directory is in the Python path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
)

from src.utils.environment import setup_logging, get_env_config
from src.application.services import QueryService
from src.adapters.factories import create_embedding_service, create_vector_repository

# --- API Setup ---
setup_logging()
app = FastAPI(
    title="CodeCraft AI API",
    description="API for interacting with the CodeCraft AI knowledge base.",
    version="1.0.0",
)

# --- Dependency Injection ---
try:
    config = get_env_config()["rag_pipeline"]
    embedding_service = create_embedding_service(config)
    vector_repository = create_vector_repository(
        config["vector_store"], config["embedding_dimension"]
    )
    query_service = QueryService(
        embedding_service=embedding_service, vector_repository=vector_repository
    )
    logging.info("API dependencies initialized successfully.")
except Exception as e:
    logging.critical(f"Failed to initialize API dependencies: {e}", exc_info=True)
    query_service = None  # Prevent the app from starting if dependencies fail


# --- API Models (Data Transfer Objects) ---
class QueryRequest(BaseModel):
    query: str = Field(
        ..., min_length=3, description="The question to ask the knowledge base."
    )
    top_k: int = Field(
        default=3, gt=0, le=10, description="The number of results to return."
    )


class ChunkResponse(BaseModel):
    document_id: str
    content: str
    metadata: dict


class QueryResponse(BaseModel):
    results: List[ChunkResponse]


# --- API Endpoints ---
@app.on_event("startup")
async def startup_event():
    if not query_service:
        raise RuntimeError("QueryService not available. Application startup failed.")
    logging.info("Application startup complete.")


@app.post("/query", response_model=QueryResponse)
async def search_knowledge_base(request: QueryRequest):
    """
    Receives a query and returns the most relevant document chunks from the knowledge base.
    """
    try:
        logging.info(f"Received API query: {request.query}")
        retrieved_chunks = query_service.search(
            query=request.query, top_k=request.top_k
        )

        # Convert domain entities to API response models
        response_chunks = [ChunkResponse(**chunk.dict()) for chunk in retrieved_chunks]

        return QueryResponse(results=response_chunks)
    except Exception as e:
        logging.error(f"An error occurred during query processing: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing the query.",
        )


@app.get("/health")
async def health_check():
    """
    Simple health check endpoint to confirm the API is running.
    """
    return {"status": "ok"}
