from unittest.mock import patch


@patch("scripts.run_rag_ingestion.get_config")
@patch("scripts.run_rag_ingestion.create_data_source")
@patch("scripts.run_rag_ingestion.create_chunking_strategy")
@patch("scripts.run_rag_ingestion.create_embedding_service")
@patch("scripts.run_rag_ingestion.create_vector_repository")
@patch("scripts.run_rag_ingestion.IngestionService")
def test_ingestion_pipeline_orchestration(
    MockIngestionService,
    mock_create_repo,
    mock_create_embedder,
    mock_create_chunker,
    mock_create_source,
    mock_get_config,
):
    """
    Verify that the main script correctly uses factories to build and run the service.
    """
    from scripts.run_rag_ingestion import main as run_ingestion_main

    mock_config = {
        "data_source": {"type": "file_system"},
        "chunking_strategy": {"type": "langchain"},
        "embedding_service": {"type": "bedrock"},
        "vector_repository": {"type": "faiss"},
    }
    mock_get_config.return_value = mock_config
    mock_service_instance = MockIngestionService.return_value

    # Act: Run the main function of the script
    run_ingestion_main()

    # Assert: Verify that the script behaved as expected
    mock_get_config.assert_called_once()
    mock_create_source.assert_called_once_with(mock_config["data_source"])
    mock_create_chunker.assert_called_once_with(mock_config["chunking_strategy"])
    mock_create_embedder.assert_called_once_with(mock_config["embedding_service"])
    mock_create_repo.assert_called_once_with(mock_config["vector_repository"])
    MockIngestionService.assert_called_once_with(
        data_source=mock_create_source.return_value,
        chunking_strategy=mock_create_chunker.return_value,
        embedding_service=mock_create_embedder.return_value,
        vector_repository=mock_create_repo.return_value,
    )
    mock_service_instance.ingest.assert_called_once()
