import sys
import os
import unittest
from unittest.mock import patch, MagicMock, mock_open
import numpy as np
import shutil
import tempfile
import json

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.adapters.vector_storage.faiss_vector_repository import FaissVectorRepository  # noqa: E402
from src.domain.entities.chunk import Chunk  # noqa: E402


class TestFaissVectorRepository(unittest.TestCase):
    """
    Tests the FaissVectorRepository adapter.
    This is an integration test at the boundary of our application. We mock the
    external `faiss` library to ensure our adapter behaves correctly without
    needing a real Faiss index on disk.
    """

    def setUp(self):
        """Set up a fresh repository for each test."""
        self.test_dir = tempfile.mkdtemp()
        self.persist_path = os.path.join(self.test_dir, "test_faiss_index.bin")

        # We patch 'faiss' in setUp to control its behavior for all tests in this class.
        self.faiss_patcher = patch(
            "src.adapters.vector_storage.faiss_vector_repository.faiss"
        )
        self.mock_faiss = self.faiss_patcher.start()

        # Mock the behavior of the faiss index object
        self.mock_index = MagicMock()
        self.mock_index.ntotal = 0
        self.mock_faiss.IndexFlatL2.return_value = self.mock_index
        self.mock_faiss.read_index.return_value = self.mock_index

        self.repository = FaissVectorRepository(
            embedding_dim=128, persist_path=self.persist_path
        )

    def tearDown(self):
        """Stop the patcher after each test."""
        self.faiss_patcher.stop()
        shutil.rmtree(self.test_dir)

    def test_add_chunks_to_index(self):
        """Verify that chunks are correctly added to the mocked faiss index."""
        # Arrange
        chunks = [
            Chunk(id="c1", document_id="d1", content="content1"),
            Chunk(id="c2", document_id="d1", content="content2"),
        ]
        chunks[0].embedding = np.array([0.1, 0.2], dtype="float32")
        chunks[1].embedding = np.array([0.3, 0.4], dtype="float32")

        # Act
        self.repository.add(chunks)

        # Assert
        self.assertEqual(self.mock_index.add.call_count, 1)
        # Check that the embeddings were stacked and passed to faiss
        np.testing.assert_array_equal(
            self.mock_index.add.call_args[0][0],
            np.array([[0.1, 0.2], [0.3, 0.4]], dtype="float32"),
        )
        self.assertEqual(len(self.repository.id_map), 2)
        self.assertEqual(self.repository.id_map[0], "c1")

    def test_search_retrieves_correct_chunks(self):
        """Verify that a query returns the correct chunk IDs based on mocked search results."""
        # Arrange
        # Pre-populate the repository's internal state for the query test
        self.repository.id_map = ["c1", "c2", "c3"]
        self.mock_index.ntotal = 3
        query_embedding = np.array([0.1, 0.2], dtype="float32")
        # Mock the return of faiss.search to be (distances, indices)
        self.mock_index.search.return_value = (
            np.array([[0.1, 0.5]]),
            np.array([[2, 0]]),
        )

        # Act
        results = self.repository.search(query_embedding, top_k=2)

        # Assert
        self.mock_index.search.assert_called_once()
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].id, "c3")  # Index 2 corresponds to c3
        self.assertEqual(results[1].id, "c1")  # Index 0 corresponds to c1

    @patch("src.adapters.vector_storage.faiss_vector_repository.os.path.exists")
    def test_persist_and_load_flow(self, mock_exists):
        """Verify that persist calls the correct faiss and json methods."""
        # Arrange
        self.repository.id_map = ["c1"]

        # Act
        self.repository.persist()

        # Assert
        self.mock_faiss.write_index.assert_called_once_with(
            self.mock_index, self.repository.index_path
        )

        mock_exists.return_value = True
        loaded_mock_index = MagicMock()
        loaded_mock_index.d = 128
        self.mock_faiss.read_index.return_value = loaded_mock_index

        with patch("builtins.open", mock_open(read_data=json.dumps(["c1"]))):
            repo = FaissVectorRepository.load(self.persist_path, embedding_dim=128)

        self.mock_faiss.read_index.assert_called_with(self.repository.index_path)
        self.assertEqual(repo.embedding_dim, 128)


if __name__ == "__main__":
    unittest.main()
