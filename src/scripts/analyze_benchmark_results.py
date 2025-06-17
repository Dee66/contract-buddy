import json
import os
import sys
from src.utils.environment import get_mode, setup_logging

def safe_fmt(val):
    return f"{val:.2f}" if isinstance(val, (int, float)) else "N/A"

def main():
    setup_logging()
    logging = __import__("logging")
    mode = get_mode()
    logging.info(f"Analyzing benchmark results in {mode.upper()} mode")

    results_path = "data/clean/hyperparam_sweep_results.json"
    if not os.path.exists(results_path):
        logging.error(f"Results file not found: {results_path}")
        sys.exit(1)

    try:
        with open(results_path, "r", encoding="utf-8") as f:
            results = json.load(f)
    except Exception as e:
        logging.error(f"Could not load results file: {results_path} ({e})")
        sys.exit(1)

    # NEW: Support both old (list) and new (dict with "runs") formats
    if isinstance(results, dict) and "runs" in results:
        results = results["runs"]

    if not results or not isinstance(results, list):
        logging.error("No results found to analyze or results file is not a list.")
        sys.exit(1)

    print("r   alpha dropout top-1  MRR    runtime  mem(MB)")
    print("-" * 50)
    best_top1 = float('-inf')
    best_mrr = float('-inf')
    best_entry = None
    for entry in results:
        hp = entry.get("hyperparams", {})
        metrics = entry.get("peft_retrieval", {})
        timing = entry.get("timing_seconds", 0)
        mem = entry.get("memory_usage_mb", 0)
        top1 = metrics.get("top1", None)
        mrr = metrics.get("mrr", None)
        print(f"{hp.get('r', ''):<3} {hp.get('alpha', ''):<5} {hp.get('dropout', ''):<7} "
              f"{safe_fmt(top1):<6} {safe_fmt(mrr):<6} "
              f"{safe_fmt(timing):<8} {safe_fmt(mem):<8}")
        if isinstance(top1, (int, float)) and top1 > best_top1:
            best_top1 = top1
            best_entry = entry
        if isinstance(mrr, (int, float)) and mrr > best_mrr:
            best_mrr = mrr

    logging.info("Benchmark analysis complete.")
    logging.info(f"Total runs analyzed: {len(results)}")
    if best_entry:
        logging.info(
            f"Best run: r={best_entry['hyperparams'].get('r')}, "
            f"alpha={best_entry['hyperparams'].get('alpha')}, "
            f"dropout={best_entry['hyperparams'].get('dropout')}, "
            f"top-1={best_top1}, mrr={best_mrr}"
        )
        # Register the best model in the model registry
        from src.storage.versioning import register_model
        hp = best_entry["hyperparams"]
        register_model(
            path=f"adapters/peft_adapter_r{hp.get('r','')}_a{hp.get('alpha','')}_d{hp.get('dropout','')}_e{hp.get('epochs','')}_b{hp.get('batch_size','')}",
            hyperparams=hp,
            metrics=best_entry["peft_retrieval"],
            status="active"
        )
    else:
        logging.warning("No valid best run found.")

if __name__ == "__main__":
    main()