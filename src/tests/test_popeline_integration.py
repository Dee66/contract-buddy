import unittest
import os
from src.utils.utils import read_yaml
from src.ingestion.data_ingestion import DataIngestion
from src.cleaning.data_cleaning import DataCleaning
from src.storage.versioning import DataVersioning
from src.chunking.chunker import CodeChunker
from src.embedding.embedder import CodeEmbedder
from src.storage.vectordb import VectorDB

class TestPipelineIntegration(unittest.TestCase):
    def test_pipeline_on_sample(self):
        # minimal config and a small sample file
        config = {
            "paths": {
                "clean_data": "data/clean",
                "raw_data": "data/raw"
            }
        }
        # Create a small sample file
        os.makedirs("data/clean", exist_ok=True)
        fname = "sample.txt"
        fpath = os.path.join("data/clean", fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write("def foo():\n    pass\n\ndef bar():\n    pass")
        chunker = CodeChunker(max_chunk_size=10)
        embedder = CodeEmbedder()
        vectordb = VectorDB()
        for fname in os.listdir("data/clean"):
            if not fname.endswith((".txt", ".py")):
                continue  # skip non-text files
            fpath = os.path.join("data/clean", fname)
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            chunks = chunker.chunk_text(content)
            embeddings = embedder.embed_chunks(chunks)
            vectordb.upsert(chunks, embeddings)
        # Check that something was embedded and stored
        self.assertTrue(len(vectordb.vectors) > 0)
        # Clean up
        os.remove(fpath)

if __name__ == "__main__":
    unittest.main()