import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
import random
import time
import sys

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

def load_pairs(path="data/clean/contrastive_pairs.json", max_pairs=100):
    """Load a set of positive pairs for evaluation."""
    with open(path, "r", encoding="utf-8") as f:
        pairs = json.load(f)
    return pairs[:max_pairs]

def generate_negative_pairs(pairs, num_negatives=None):
    """Generate negative pairs by mismatching the first and second elements."""
    if not pairs:
        return []
    num_negatives = num_negatives or len(pairs)
    firsts = [a for a, _ in pairs]
    seconds = [b for _, b in pairs]
    random.shuffle(seconds)
    negatives = []
    for a, b in zip(firsts, seconds):
        if a != b:
            negatives.append([a, b])
        if len(negatives) >= num_negatives:
            break
    return negatives

def evaluate_model(model: SentenceTransformer, pairs):
    """Compute average cosine similarity for pairs."""
    scores = []
    for a, b in pairs:
        emb_a = model.encode(a, convert_to_numpy=True)
        emb_b = model.encode(b, convert_to_numpy=True)
        sim = float(cosine_similarity([emb_a], [emb_b])[0][0])
        scores.append(sim)
    return float(np.mean(scores)), scores

def retrieval_metrics(model: SentenceTransformer, pairs, negatives, top_k=5):
    """
    For each anchor (a), rank all possible candidates (b's) including the true positive and negatives.
    Compute top-1, top-k accuracy and MRR.
    """
    anchors = [a for a, _ in pairs]
    positives = [b for _, b in pairs]
    candidates = positives + [b for a, b in negatives]
    metrics = {"top1": 0, "topk": 0, "mrr": 0}
    for idx, (anchor, true_b) in enumerate(zip(anchors, positives)):
        anchor_emb = model.encode(anchor, convert_to_numpy=True)
        candidate_embs = model.encode(candidates, convert_to_numpy=True)
        sims = cosine_similarity([anchor_emb], candidate_embs)[0]
        # Rank candidates by similarity
        ranked_indices = np.argsort(sims)[::-1]
        # Find the rank of the true positive
        true_idx = candidates.index(true_b)
        rank = np.where(ranked_indices == true_idx)[0][0] + 1  # 1-based
        metrics["mrr"] += 1.0 / rank
        if rank == 1:
            metrics["top1"] += 1
        if rank <= top_k:
            metrics["topk"] += 1
    n = len(anchors)
    metrics["top1"] /= n
    metrics["topk"] /= n
    metrics["mrr"] /= n
    return metrics

def main():
    pairs = load_pairs()
    negatives = generate_negative_pairs(pairs)
    results = {}

    # Timing and resource usage
    process = psutil.Process(os.getpid()) if PSUTIL_AVAILABLE else None
    start_time = time.time()
    start_mem = process.memory_info().rss if process else None

    # Evaluate base model
    print("Evaluating base model...")
    base_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    base_pos_mean, base_pos_scores = evaluate_model(base_model, pairs)
    base_neg_mean, base_neg_scores = evaluate_model(base_model, negatives)
    base_retrieval = retrieval_metrics(base_model, pairs, negatives)
    results["base_mean_similarity_positive"] = base_pos_mean
    results["base_mean_similarity_negative"] = base_neg_mean
    results["base_scores_positive"] = [float(s) for s in base_pos_scores]
    results["base_scores_negative"] = [float(s) for s in base_neg_scores]
    results["base_retrieval"] = base_retrieval

    # Evaluate PEFT-adapted model
    peft_dir = sys.argv[1] if len(sys.argv) > 1 else "peft_adapter_contrastive"
    # Always create a new model instance for PEFT
    if os.path.exists(peft_dir):
        print("Evaluating PEFT-adapted model...")
        peft_model = SentenceTransformer(peft_dir)
        peft_pos_mean, peft_pos_scores = evaluate_model(peft_model, pairs)
        peft_neg_mean, peft_neg_scores = evaluate_model(peft_model, negatives)
        peft_retrieval = retrieval_metrics(peft_model, pairs, negatives)
        results["peft_mean_similarity_positive"] = peft_pos_mean
        results["peft_mean_similarity_negative"] = peft_neg_mean
        results["peft_scores_positive"] = [float(s) for s in peft_pos_scores]
        results["peft_scores_negative"] = [float(s) for s in peft_neg_scores]
        results["peft_retrieval"] = peft_retrieval
    else:
        print(f"[INFO] PEFT adapter directory '{peft_dir}' not found. Only base model will be evaluated.")
        results["peft_mean_similarity_positive"] = None
        results["peft_mean_similarity_negative"] = None
        results["peft_scores_positive"] = None
        results["peft_scores_negative"] = None
        results["peft_retrieval"] = None

    # Timing and resource usage (end)
    end_time = time.time()
    end_mem = process.memory_info().rss if process else None
    results["timing_seconds"] = end_time - start_time
    if start_mem is not None and end_mem is not None:
        results["memory_usage_mb"] = (end_mem - start_mem) / (1024 * 1024)

    # Save results
    with open("data/clean/eval_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("Evaluation complete. Results saved to data/clean/eval_results.json")
    print(f"Base model mean similarity (positive): {results['base_mean_similarity_positive']:.4f}")
    print(f"Base model mean similarity (negative): {results['base_mean_similarity_negative']:.4f}")
    print(f"Base model retrieval: top-1={results['base_retrieval']['top1']:.2f}, top-5={results['base_retrieval']['topk']:.2f}, MRR={results['base_retrieval']['mrr']:.2f}")
    if results["peft_mean_similarity_positive"] is not None:
        print(f"PEFT model mean similarity (positive): {results['peft_mean_similarity_positive']:.4f}")
        print(f"PEFT model mean similarity (negative): {results['peft_mean_similarity_negative']:.4f}")
        print(f"PEFT model retrieval: top-1={results['peft_retrieval']['top1']:.2f}, top-5={results['peft_retrieval']['topk']:.2f}, MRR={results['peft_retrieval']['mrr']:.2f}")
    else:
        print("PEFT model was not evaluated (adapter missing).")
    print(f"Total evaluation time: {results['timing_seconds']:.2f} seconds")
    if "memory_usage_mb" in results:
        print(f"Net memory usage: {results['memory_usage_mb']:.2f} MB")

if __name__ == "__main__":
    main()
