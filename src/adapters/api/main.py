import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from typing import List

# No more sys.path manipulation. This is handled by pytest.ini for tests
# and the execution environment (e.g., Docker's PYTHONPATH) for runtime.
from src.adapters.environment import ConfigLoader, setup_logging
from src.application.services import QueryService
from src.domain.entities.chunk import Chunk
from src.domain.entities.query import Query, QueryResult
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


# --- Lifespan Management for Application State ---
# This is the modern replacement for @app.on_event("startup")
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages application startup and shutdown logic.
    """
    setup_logging()
    logging.info("API starting up...")

    config_loader = ConfigLoader()
    config = config_loader.get_config()

    # The Composition Root passes the specific sub-configuration to each factory.
    embedding_service = create_embedding_service(config.embedding_service)
    vector_repository = create_vector_repository(
        config.vector_repository, embedding_service
    )

    app.state.query_service = QueryService(
        embedding_service=embedding_service, vector_repository=vector_repository
    )
    logging.info("API dependencies initialized successfully.")

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


@app.post("/query", response_model=QueryResult, tags=["RAG"])
def query_endpoint(query: Query, request: Request):
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
