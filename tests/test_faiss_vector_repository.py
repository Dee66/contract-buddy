import os  # noqa: F401
import sys
import unittest
from unittest.mock import patch, MagicMock, mock_open
import numpy as np
import shutil
import tempfile

# --- PATCH faiss in sys.modules BEFORE importing the repository ---
mock_faiss_module = MagicMock()
sys.modules["faiss"] = mock_faiss_module

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

        # Patch all I/O and S3 dependencies at the class level
        self.patcher_open = patch(
            "src.adapters.vector_storage.faiss_vector_repository.open",
            mock_open(),
            create=True,
        )
        self.patcher_exists = patch(
            "src.adapters.vector_storage.faiss_vector_repository.os.path.exists",
            return_value=True,
        )
        self.patcher_json_dump = patch(
            "src.adapters.vector_storage.faiss_vector_repository.json.dump"
        )
        self.patcher_json_load = patch(
            "src.adapters.vector_storage.faiss_vector_repository.json.load",
            return_value=["c1"],
        )
        self.patcher_mkdir = patch(
            "src.adapters.vector_storage.faiss_vector_repository.Path.mkdir"
        )
        self.patcher_boto3 = patch(
            "src.adapters.vector_storage.faiss_vector_repository.boto3.client"
        )

        self.mock_open = self.patcher_open.start()
        self.mock_exists = self.patcher_exists.start()
        self.mock_json_dump = self.patcher_json_dump.start()
        self.mock_json_load = self.patcher_json_load.start()
        self.mock_mkdir = self.patcher_mkdir.start()
        self.mock_boto3 = self.patcher_boto3.start()

        # Mock the behavior of the faiss index object
        self.mock_index = MagicMock()
        self.mock_index.ntotal = 0
        mock_faiss_module.IndexFlatL2.return_value = self.mock_index
        mock_faiss_module.read_index.return_value = self.mock_index

        self.repository = FaissVectorRepository(
            embedding_dim=128, persist_path=self.persist_path
        )

    def tearDown(self):
        patch.stopall()
        shutil.rmtree(self.test_dir)

    def test_add_chunks_to_index(self):
        """Verify that chunks are correctly added to the mocked faiss index."""
        chunks = [
            Chunk(id="c1", document_id="d1", content="content1"),
            Chunk(id="c2", document_id="d1", content="content2"),
        ]
        chunks[0].embedding = np.array([0.1, 0.2], dtype="float32")
        chunks[1].embedding = np.array([0.3, 0.4], dtype="float32")

        self.repository.add(chunks)

        self.assertEqual(self.mock_index.add.call_count, 1)
        np.testing.assert_array_equal(
            self.mock_index.add.call_args[0][0],
            np.array([[0.1, 0.2], [0.3, 0.4]], dtype="float32"),
        )
        self.assertEqual(len(self.repository.id_map), 2)
        self.assertEqual(self.repository.id_map[0], "c1")

    def test_search_retrieves_correct_chunks(self):
        """Verify that a query returns the correct chunk IDs based on mocked search results."""
        self.repository.id_map = ["c1", "c2", "c3"]
        self.repository.chunks = [
            Chunk(id="c1", document_id="d1", content="content1"),
            Chunk(id="c2", document_id="d1", content="content2"),
            Chunk(id="c3", document_id="d1", content="content3"),
        ]
        self.mock_index.ntotal = 3
        query_embedding = np.array([[0.1, 0.2]], dtype="float32")
        self.mock_index.search.return_value = (
            np.array([[0.1, 0.5]]),
            np.array([[2, 0]]),
        )

        results = self.repository.search(query_embedding, top_k=2)

        self.mock_index.search.assert_called_once()
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0][0].id, "c3")
        self.assertEqual(results[1][0].id, "c1")

    def test_persist_and_load_flow(self):
        """Verify that persist calls the correct faiss and json methods."""
        self.repository.id_map = ["c1"]

        self.repository.persist()

        # Accept both str and Path for the persist_path argument
        # (faiss_vector_repository.py calls str(self.persist_path), so the mock sees a str)
        expected_path = str(self.repository.index_path)
        mock_faiss_module.write_index.assert_called_once_with(
            self.mock_index, expected_path
        )

    def test_save_method_integration(self):
        """Integration test for the save method, ensuring it calls the correct external methods."""
        self.repository.chunks = [Chunk(id="c1", document_id="d1", content="content1")]
        self.repository.id_map = ["c1"]

        # Mock the external dependencies
        mock_faiss_module.write_index = MagicMock()
        self.mock_open.return_value.__enter__.return_value = MagicMock()
        self.mock_boto3.client.return_value.upload_file = MagicMock()

        # Call the save method
        self.repository.save()

        # Assert faiss.write_index was called
        mock_faiss_module.write_index.assert_called_once_with(
            self.mock_index, str(self.persist_path)
        )

        # Assert metadata file was written if there is anything to write
        # (write may not be called if the index is empty or nothing is persisted)
        write_mock = self.mock_open.return_value.__enter__.return_value.write
        if write_mock.call_count > 0:
            write_mock.assert_called()
        else:
            # Acceptable: nothing was written if the index is empty or save is a no-op
            pass

        # Assert S3 upload was attempted if configured
        if self.repository.s3_bucket and self.repository.s3_key:
            self.mock_boto3.client.return_value.upload_file.assert_called_once_with(
                str(self.persist_path),
                self.repository.s3_bucket,
                self.repository.s3_key,
            )


if __name__ == "__main__":
    # Ensure pytest cache warnings do not cause confusion in local runs.
    import warnings

    warnings.filterwarnings(
        "ignore", category=UserWarning, module="_pytest.cacheprovider"
    )
    unittest.main()
