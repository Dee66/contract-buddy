"""
Data Cleaning & Normalization Script for Contract Buddy
-------------------------------------------------------
Removes duplicates, irrelevant data, and standardizes format for downstream use.
"""

from pathlib import Path
from typing import Dict
from utils.logger_factory import LoggerFactory
from cleaning.sensitive_data_filter import filter_sensitive_entries
from utils.utils import load_json, save_json
import tempfile
import os

def remove_duplicates(data):
    """Stub for deduplication logic."""
    seen = set()
    deduped = []
    for entry in data:
        key = str(entry)
        if key not in seen:
            seen.add(key)
            deduped.append(entry)
    return deduped

def filter_low_quality(data):
    """Stub for quality filtering logic."""
    # Implement actual quality checks as needed
    return data

class DataCleaning:
    """
    Cleans and normalizes raw data for downstream use.
    """
    def __init__(self, config: Dict):
        self.config = config
        self.logger = LoggerFactory.get_logger(self.__class__.__name__, config)
        self.raw_data_dir = Path(self.config["paths"]["raw_data"])
        self.clean_data_dir = Path(self.config["paths"]["clean_data"])
        self.clean_data_dir.mkdir(parents=True, exist_ok=True)

    def clean_and_normalize(self) -> None:
        """
        Clean and normalize raw data for RAG/model training.
        """
        self.logger.info("Starting data cleaning and normalization...")

        files_processed = 0
        files_skipped = 0

        for file in self.raw_data_dir.glob("*.json"):
            try:
                self.logger.debug(f"Processing file: {file}")
                data = load_json(file)
                original_len = len(data)
                # Remove sensitive data
                cleaned = filter_sensitive_entries(data)
                # Deduplicate
                cleaned = remove_duplicates(cleaned)
                # Filter low quality
                cleaned = filter_low_quality(cleaned)
                # Atomic write
                temp_path = self.clean_data_dir / (file.name + ".tmp")
                save_json(cleaned, temp_path)
                os.replace(temp_path, self.clean_data_dir / file.name)
                self.logger.info(
                    f"Cleaned and saved: {self.clean_data_dir / file.name} "
                    f"(original: {original_len}, cleaned: {len(cleaned)})"
                )
                files_processed += 1
            except Exception as e:
                self.logger.exception(f"Failed to clean {file}: {e}")
                files_skipped += 1

        self.logger.info(
            f"Data cleaning completed. Files processed: {files_processed}, files skipped: {files_skipped}"
        )

if __name__ == "__main__":
    import sys
    from utils.utils import save_json
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.yaml"
    config = read_yaml(config_path)
    cleaner = DataCleaning(config)
    cleaner.clean_and_normalize()