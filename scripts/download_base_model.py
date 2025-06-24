from transformers import AutoModelForSequenceClassification, AutoTokenizer
import sys
import os

# 🟦 NOTE: Ensure src is on the Python path for all environments (dev, staging, prod)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# 🟩 GOOD: Use canonical config and logging setup for the whole repo
from src.adapters.environment import setup_logging, get_mode, ConfigLoader


def main():
    setup_logging()
    import logging

    mode = get_mode()
    config = ConfigLoader().get_config()
    base_model_name = config.embedding.model_name
    logging.info(f"Downloading base model: {base_model_name} (mode: {mode})")
    try:
        # Download and cache the model and tokenizer
        AutoTokenizer.from_pretrained(base_model_name)
        AutoModelForSequenceClassification.from_pretrained(base_model_name)
        logging.info("Base model and tokenizer downloaded and cached successfully.")
    except Exception as e:
        logging.error(f"Failed to download base model: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
