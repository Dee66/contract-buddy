"""
Data Ingestion Script for CodeCraft AI
----------------------------------------
Fetches, validates, and stores data from approved sources for RAG and model fine-tuning.
"""

from pathlib import Path
from typing import Dict
from src.utils.logger_factory import LoggerFactory
from src.ingestion.sources.github import fetch_github_repos
from src.ingestion.sources.docs import fetch_docs
from src.ingestion.sources.stackoverflow import fetch_stackoverflow
from src.utils.utils import save_json

class DataIngestion:
    def __init__(self, config: Dict):
        self.config = config
        self.logger = LoggerFactory.get_logger(self.__class__.__name__, config)

    def fetch_and_store(self):
        raw_data_dir = Path(self.config["paths"]["raw_data"])
        raw_data_dir.mkdir(parents=True, exist_ok=True)

        # Fetch GitHub repos if enabled
        if self.config["sources"].get("github", {}).get("enabled", False):
            repos = self.config["sources"]["github"].get("repo_list", [])
            try:
                self.logger.debug(f"Fetching GitHub repos: {repos}")
                github_data = fetch_github_repos(repos)
                save_json(github_data, raw_data_dir / "github_repos.json")
                self.logger.info(f"Saved GitHub data to {raw_data_dir / 'github_repos.json'}")
            except Exception as e:
                self.logger.error(f"Failed to fetch GitHub repos: {e}")

        # Fetch docs if enabled
        if self.config["sources"].get("docs", {}).get("enabled", False):
            doc_urls = self.config["sources"]["docs"].get("doc_urls", [])
            try:
                self.logger.debug(f"Fetching documentation URLs: {doc_urls}")
                docs_data = fetch_docs(doc_urls)
                save_json(docs_data, raw_data_dir / "docs.json")
                self.logger.info(f"Saved docs data to {raw_data_dir / 'docs.json'}")
            except Exception as e:
                self.logger.error(f"Failed to fetch docs: {e}")

        # Fetch Stack Overflow if enabled
        if self.config["sources"].get("stackoverflow", {}).get("enabled", False):
            api_key = self.config["sources"]["stackoverflow"].get("api_key", "")
            try:
                self.logger.debug("Fetching Stack Overflow data")
                so_data = fetch_stackoverflow(api_key)
                save_json(so_data, raw_data_dir / "stackoverflow.json")
                self.logger.info(f"Saved Stack Overflow data to {raw_data_dir / 'stackoverflow.json'}")
            except Exception as e:
                self.logger.error(f"Failed to fetch Stack Overflow data: {e}")

if __name__ == "__main__":
    import sys
    from utils.utils import read_yaml
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.yaml"
    config = read_yaml(config_path)
    DataIngestion(config).fetch_and_store()