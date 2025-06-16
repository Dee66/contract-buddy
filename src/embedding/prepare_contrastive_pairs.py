import json
import random
import os
import re

def load_chunks(path="data/clean/docs.json"):
    with open(path, "r", encoding="utf-8") as f:
        docs = json.load(f)
    # Assume each doc has a 'content' field
    return [doc["content"] for doc in docs if "content" in doc]

def create_positive_pairs(chunks, num_pairs=50):
    pairs = []
    n = len(chunks)
    for _ in range(num_pairs):
        a, b = random.sample(chunks, 2)
        pairs.append([a, b])
    return pairs

def main():
    chunks = load_chunks()
    if len(chunks) < 2:
        print("Not enough chunks to create pairs. Please add more data to data/clean/docs.json.")
        return
    pairs = create_positive_pairs(chunks, num_pairs=min(100, len(chunks) * 5))
    with open("data/clean/contrastive_pairs.json", "w", encoding="utf-8") as f:
        json.dump(pairs, f, indent=2)
    print(f"Saved {len(pairs)} positive pairs to data/clean/contrastive_pairs.json")

if __name__ == "__main__":
    main()