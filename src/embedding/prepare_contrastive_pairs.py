import json
import os
import sys
from pathlib import Path
from src.utils.environment import get_mode, setup_logging

def load_chunks(path="data/clean/docs.json"):
    with open(path, "r", encoding="utf-8") as f:
        docs = json.load(f)
    return [doc["content"] for doc in docs if "content" in doc]

def create_positive_pairs(chunks, num_pairs=100):
    import random
    pairs = []
    n = len(chunks)
    for _ in range(num_pairs):
        a, b = random.sample(chunks, 2)
        pairs.append([a, b])
    return pairs

def main():
    setup_logging()
    logging = __import__("logging")
    mode = get_mode()
    if mode == "dev":
        num_pairs = 200
        logging.info("Preparing contrastive pairs in DEV mode (200 pairs)")
    else:
        num_pairs = 1000
        logging.info("Preparing contrastive pairs in PROD mode (1000 pairs)")

    input_path = "data/clean/docs.json"
    output_path = "data/clean/contrastive_pairs.json"
    Path(os.path.dirname(output_path)).mkdir(parents=True, exist_ok=True)

    if not os.path.exists(input_path):
        logging.error(f"Input file missing: {input_path}")
        sys.exit(1)

    chunks = load_chunks(input_path)
    if len(chunks) < 2:
        logging.error("Not enough chunks to create pairs. Please add more data to data/clean/docs.json.")
        sys.exit(1)

    pairs = create_positive_pairs(chunks, num_pairs=min(num_pairs, len(chunks) * 5))
    if len(pairs) < 2:
        logging.error("Failed to create enough contrastive pairs.")
        sys.exit(1)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(pairs, f, indent=2)
    logging.info(f"Saved {len(pairs)} positive pairs to {output_path}")
    logging.info("Contrastive pairs creation complete and saved to data/clean/contrastive_pairs.json")

if __name__ == "__main__":
    main()