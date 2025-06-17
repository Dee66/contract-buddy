from transformers import AutoModelForSequenceClassification, AutoTokenizer
from src.utils.environment import setup_logging, get_mode
import sys

def main():
    setup_logging()
    logging = __import__("logging")
    mode = get_mode()
    base_model_name = "sentence-transformers/all-MiniLM-L6-v2"
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