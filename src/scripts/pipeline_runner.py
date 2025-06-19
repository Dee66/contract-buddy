import os
from src.utils.environment import get_mode, setup_logging, get_config, get_env_config
from src.ingestion.data_ingestion import DataIngestion
from src.cleaning.data_cleaning import DataCleaning
from src.storage.versioning import DataVersioning
from src.chunking.chunker import CodeChunker
from src.embedding.embedder import CodeEmbedder
from src.storage.vectordb import VectorDB

def infer_language_and_framework(filename: str, config) -> (str, str):
    ext = os.path.splitext(filename)[1].lower()
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
    }
    if "language_overrides" in config and filename in config["language_overrides"]:
        return config["language_overrides"][filename]
    return ext_map.get(ext, ("text", None))

def main(config_path="config.yaml"):
    setup_logging()
    mode = get_mode()
    logging = __import__("logging")
    config = get_config(config_path)
    env_config = get_env_config(config_path)
    logging.info(f"Starting data pipeline in {mode.upper()} mode...")

    DataIngestion(config).fetch_and_store()
    DataCleaning(config).clean_and_normalize()
    DataVersioning(config).version_data()

    chunker = CodeChunker(max_chunk_size=512)
    embedder = CodeEmbedder()
    vectordb = VectorDB()

    clean_data_dir = env_config.get("clean_data_dir", config.get("paths", {}).get("clean_data", "data/clean/"))
    files = os.listdir(clean_data_dir)
    if mode == "dev":
        files = files[:2]
        logging.info(f"DEV mode: Only processing first {len(files)} files in {clean_data_dir}")

    for fname in files:
        fpath = os.path.join(clean_data_dir, fname)
        language, framework = infer_language_and_framework(fname, config)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        chunks = chunker.chunk_text(content, language=language, framework=framework)
        if mode == "dev":
            chunks = chunks[:10]
        embeddings = embedder.embed_chunks(chunks)
        vectordb.upsert(chunks, embeddings)

    logging.info("Data pipeline completed successfully.")

if __name__ == "__main__":
    setup_logging()
    mode = get_mode()
    logging = __import__("logging")
    logging.info(f"Pipeline runner started in {mode.upper()} mode")
    main()
    logging.info("Pipeline runner completed successfully")