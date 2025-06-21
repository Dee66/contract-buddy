"""
Data Versioning Script for CodeCraft AI
-----------------------------------------
Handles dataset versioning for reproducibility and auditability.
"""

from pathlib import Path
from typing import Dict
from src.utils.logger_factory import LoggerFactory
import subprocess
import datetime
import json
import os
from datetime import datetime
import tempfile
import shutil

REGISTRY_PATH = "data/clean/model_registry.json"

def load_registry():
    if not os.path.exists(REGISTRY_PATH):
        return []
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_registry(registry):
    # Write to a temp file, then move atomically
    dir_name = os.path.dirname(REGISTRY_PATH)
    with tempfile.NamedTemporaryFile("w", dir=dir_name, delete=False, encoding="utf-8") as tf:
        json.dump(registry, tf, indent=2)
        tempname = tf.name
    shutil.move(tempname, REGISTRY_PATH)

def validate_entry(entry):
    required_keys = {"version", "path", "hyperparams", "metrics", "status", "timestamp"}
    if not isinstance(entry, dict):
        raise ValueError("Registry entry must be a dict.")
    missing = required_keys - set(entry.keys())
    if missing:
        raise ValueError(f"Registry entry missing keys: {missing}")
    if entry["status"] not in {"active", "deprecated"}:
        raise ValueError("Status must be 'active' or 'deprecated'.")
    # Add more validation as needed (e.g., types, metrics structure)

def register_model(path, hyperparams, metrics, status="active"):
    registry = load_registry()
    version = datetime.now().strftime("%Y%m%d-%H%M%S-%f")  # Add microseconds
    if status == "active":
        for entry in registry:
            entry["status"] = "deprecated"
    entry = {
        "version": version,
        "path": path,
        "hyperparams": hyperparams,
        "metrics": metrics,
        "status": status,
        "timestamp": datetime.now().isoformat()
    }
    validate_entry(entry)
    registry.append(entry)
    save_registry(registry)
    return version

def list_models():
    return load_registry()

def set_active(version):
    registry = load_registry()
    found = False
    for entry in registry:
        if entry["version"] == version:
            entry["status"] = "active"
            found = True
        else:
            entry["status"] = "deprecated"
    save_registry(registry)
    return found

def rollback_to(version):
    return set_active(version)

class DataVersioning:
    """
    Handles dataset versioning for reproducibility and auditability.
    """
    def __init__(self, config: Dict):
        self.config = config
        self.logger = LoggerFactory.get_logger(self.__class__.__name__, config)
        self.clean_data_dir = Path(self.config["paths"]["clean_data"])

    def version_data(self) -> None:
        """
        Version the cleaned data directory using Git or DVC.
        """
        self.logger.info("Starting data versioning...")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            # Example: Using Git for versioning
            subprocess.run(["git", "add", str(self.clean_data_dir)], check=True)
            commit_msg = f"Update cleaned data version ({self.clean_data_dir}) at {timestamp}"
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            self.logger.info(f"Data versioned and committed: {self.clean_data_dir} at {timestamp}")
            # For DVC, you could add: subprocess.run(["dvc", "add", str(self.clean_data_dir)], check=True)
        except subprocess.CalledProcessError as e:
            self.logger.exception(f"Versioning failed: {e}")
        except Exception as e:
            self.logger.exception(f"Unexpected error during versioning: {e}")

        self.logger.info("Data versioning completed.")

if __name__ == "__main__":
    import sys
    from utils.utils import read_yaml
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.yaml"
    config = read_yaml(config_path)
    versioner = DataVersioning(config)
    versioner.version_data()