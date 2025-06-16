import os
from utils.utils import read_yaml
from ingestion.data_ingestion import DataIngestion
from cleaning.data_cleaning import DataCleaning
from storage.versioning import DataVersioning
from chunking.chunker import CodeChunker
from embedding.embedder import CodeEmbedder
from storage.vectordb import VectorDB

# --- Language and Framework Inference Helpers ---
def infer_language_and_framework(filename: str, config) -> (str, str):
    ext = os.path.splitext(filename)[1].lower()
    # Map file extensions to languages/frameworks
    ext_map = {
        ".py": ("python", None),
        ".js": ("javascript", "react" if "react" in filename.lower() else None),
        ".jsx": ("javascript", "react"),
        ".ts": ("typescript", "angular" if "angular" in filename.lower() else None),
        ".tsx": ("typescript", "react"),
        ".java": ("java", None),
        ".kt": ("kotlin", None),
        ".c": ("c", None),
        ".cpp": ("cpp", None),
        ".cs": ("csharp", None),
        ".go": ("go", None),
        ".rb": ("ruby", None),
        ".php": ("php", None),
        ".html": ("html", None),
        ".json": ("json", None),
        # Add more as needed
    }
    # Use config or metadata if available
    if "language_overrides" in config and filename in config["language_overrides"]:
        return config["language_overrides"][filename]
    return ext_map.get(ext, ("text", None))

def main(config_path="config.yaml"):
    config = read_yaml(config_path)
    print("Starting data pipeline...")

    DataIngestion(config).fetch_and_store()
    DataCleaning(config).clean_and_normalize()
    DataVersioning(config).version_data()

    # --- Chunking, Embedding, and Vector DB Integration ---
    chunker = CodeChunker(max_chunk_size=512)
    embedder = CodeEmbedder()
    vectordb = VectorDB()

    clean_data_dir = config["paths"]["clean_data"]
    for fname in os.listdir(clean_data_dir):
        fpath = os.path.join(clean_data_dir, fname)
        language, framework = infer_language_and_framework(fname, config)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        chunks = chunker.chunk_text(content, language=language, framework=framework)
        embeddings = embedder.embed_chunks(chunks)
        vectordb.upsert(chunks, embeddings)

    print("Data pipeline completed successfully.")

if __name__ == "__main__":
    main()