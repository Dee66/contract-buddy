from pathlib import Path
import logging
import yaml
import json
import tempfile
import os

def setup_logging(log_dir: str, log_file: str = "pipeline.log", level: str = "INFO"):
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_path = Path(log_dir) / log_file
    logging.basicConfig(
        filename=log_path,
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s"
    )

def read_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def save_json(data, path):
    # Atomic write: write to temp file then move
    temp_path = str(path) + ".tmp"
    with open(temp_path, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(temp_path, path)

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)