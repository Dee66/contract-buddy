import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List

from src.adapters.config_manager import ConfigManager
from src.application.services.query_service import QueryService  # <-- FIXED IMPORT
from src.domain.entities.chunk import Chunk
from src.adapters.factories.factories import (
    create_embedding_service,
    create_vector_repository,
)


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


# --- Configuration Management ---
config_manager = ConfigManager()


def get_app_config():
    return config_manager.config


def get_api_key(request: Request):
    return request.headers.get("X-API-Key")


# --- Lifespan Management for Application State ---
# This is the modern replacement for @app.on_event("startup")
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages application startup and shutdown logic.
    """
    config_manager.load()
    config = config_manager.config

    embedding_service = create_embedding_service(config.embedding_service)
    vector_repository = create_vector_repository(
        config.vector_repository, embedding_service
    )

    app.state.query_service = QueryService(
        embedding_service=embedding_service, vector_repository=vector_repository
    )
    logging.info(
        f"API dependencies initialized. Config version: {config_manager.last_version or 'unknown'}"
    )

    # The application runs until it is shut down
    yield
    # --- Shutdown logic would go here ---
    logging.info("API shutting down.")


app = FastAPI(
    title="CodeCraft AI API",
    description="API for interacting with the CodeCraft AI RAG system.",
    version="1.0.0",
    lifespan=lifespan,
)

# --- API Endpoints ---


@app.get("/health", status_code=200, tags=["Health"])
def health_check():
    """Simple health check endpoint to confirm the API is running."""
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse, tags=["RAG"])
def query_endpoint(query: QueryRequest, request: Request):
    """
    Receives a query and returns the most relevant document chunks.
    """
    query_service = request.app.state.query_service
    if not query_service:
        raise HTTPException(status_code=503, detail="Service not available.")

    try:
        retrieved_chunks: List[Chunk] = query_service.search(
            query=query.query, top_k=query.top_k
        )
        response_chunks = [
            ChunkResponse(
                document_id=chunk.document_id,
                content=chunk.content,
                metadata=chunk.metadata,
            )
            for chunk in retrieved_chunks
        ]
        return QueryResponse(results=response_chunks)
    except Exception as e:
        logging.error(f"Error during query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error.")


@app.get("/config")
def show_config(cfg=Depends(get_app_config)):
    """
    Expose config for debugging (remove or secure in production)
    """
    return cfg.dict()


@app.post("/reload-config", status_code=200, tags=["Admin"])
def reload_config(request: Request, api_key: str = Depends(get_api_key)):
    """
    Reloads configuration from SSM Parameter Store at runtime.
    Requires a valid X-API-Key header.
    """
    expected_api_key = config_manager.get_current_api_key()
    if not api_key or api_key != expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key."
        )

    try:
        config_manager.load(force_reload=True)
        config = config_manager.config
        logging.info(
            f"Config reloaded via /reload-config. New version: {config_manager.last_version or 'unknown'}"
        )
        # Optionally, re-initialize downstream services if config affects them
        embedding_service = create_embedding_service(config.embedding_service)
        vector_repository = create_vector_repository(
            config.vector_repository, embedding_service
        )
        request.app.state.query_service = QueryService(
            embedding_service=embedding_service, vector_repository=vector_repository
        )
        return {"status": "reloaded", "config_version": config_manager.last_version}
    except Exception as e:
        logging.error(f"Failed to reload config: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to reload config")
