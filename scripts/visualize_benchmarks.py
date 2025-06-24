import json
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
from src.utils.environment import setup_logging


def safe_fmt(val):
    return f"{val:.2f}" if isinstance(val, (int, float)) else "N/A"


def visualize_benchmarks(results_path="data/clean/hyperparam_sweep_results.json"):
    import logging

    if not os.path.exists(results_path):
        logging.error(f"Results file not found: {results_path}")
        sys.exit(1)

    try:
        with open(results_path, "r", encoding="utf-8") as f:
            results = json.load(f)
    except Exception as e:
        logging.error(f"Could not load results file: {results_path} ({e})")
        sys.exit(1)

    if isinstance(results, dict) and "runs" in results:
        results = results["runs"]

    if not results or not isinstance(results, list):
        logging.error("No results found to visualize or results file is not a list.")
        sys.exit(1)

    filtered = [
        r
        for r in results
        if (
            "peft_retrieval" in r
            and r["peft_retrieval"] is not None
            and isinstance(r["peft_retrieval"].get("top1"), (int, float))
            and isinstance(r.get("timing_seconds"), (int, float))
            and isinstance(r.get("estimated_cost_usd"), (int, float))
        )
    ]
    if not filtered:
        logging.error(
            "No valid entries with numeric 'top1', 'timing_seconds', and 'estimated_cost_usd' found for visualization."
        )
        sys.exit(1)

    top1 = [r["peft_retrieval"]["top1"] for r in filtered]
    runtime = [r["timing_seconds"] for r in filtered]
    mrr = [r["peft_retrieval"].get("mrr") for r in filtered]
    cost = [r.get("estimated_cost_usd") for r in filtered]
    labels = [
        f"r={r['hyperparams'].get('r', '')},a={r['hyperparams'].get('alpha', '')},d={r['hyperparams'].get('dropout', '')}"
        for r in filtered
    ]

    # Plot 1: Cost vs Top-1 Accuracy
    plt.figure(figsize=(10, 6))
    scatter1 = sns.scatterplot(
        x=cost, y=top1, hue=mrr, palette="viridis", s=100, legend="brief"
    )
    for i, label in enumerate(labels):
        plt.annotate(label, (cost[i], top1[i]), fontsize=8, alpha=0.7)
    plt.xlabel("Estimated Cost (USD)")
    plt.ylabel("Top-1 Accuracy")
    plt.title("PEFT Hyperparameter Sweep: Top-1 vs Cost")
    plt.colorbar(scatter1.collections[0], label="MRR")
    plt.tight_layout()
    output_path1 = "data/clean/benchmark_top1_vs_cost.png"
    plt.savefig(output_path1)
    logging.info(f"Visualization saved to {output_path1}")
    plt.close()

    # Plot 2: Cost vs Runtime
    plt.figure(figsize=(10, 6))
    scatter2 = sns.scatterplot(
        x=cost, y=runtime, hue=top1, palette="coolwarm", s=100, legend="brief"
    )
    for i, label in enumerate(labels):
        plt.annotate(label, (cost[i], runtime[i]), fontsize=8, alpha=0.7)
    plt.xlabel("Estimated Cost (USD)")
    plt.ylabel("Runtime (s)")
    plt.title("PEFT Hyperparameter Sweep: Runtime vs Cost")
    plt.colorbar(scatter2.collections[0], label="Top-1 Accuracy")
    plt.tight_layout()
    output_path2 = "data/clean/benchmark_runtime_vs_cost.png"
    plt.savefig(output_path2)
    logging.info(f"Visualization saved to {output_path2}")
    plt.close()

    # Plot 3: Top-1 vs Runtime, colored by Cost
    plt.figure(figsize=(10, 6))
    scatter3 = sns.scatterplot(
        x=runtime, y=top1, hue=cost, palette="plasma", s=100, legend="brief"
    )
    for i, label in enumerate(labels):
        plt.annotate(label, (runtime[i], top1[i]), fontsize=8, alpha=0.7)
    plt.xlabel("Runtime (s)")
    plt.ylabel("Top-1 Accuracy")
    plt.title("PEFT Hyperparameter Sweep: Top-1 vs Runtime (colored by Cost)")
    plt.colorbar(scatter3.collections[0], label="Estimated Cost (USD)")
    plt.tight_layout()
    output_path3 = "data/clean/benchmark_top1_vs_runtime_cost.png"
    plt.savefig(output_path3)
    logging.info(f"Visualization saved to {output_path3}")
    plt.close()

    # Markdown report generation
    md_path = "data/clean/benchmark_report.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# PEFT Hyperparameter Sweep Benchmark Report\n\n")
        f.write("## Plots\n")
        f.write("![Top-1 vs Cost](benchmark_top1_vs_cost.png)\n\n")
        f.write("![Runtime vs Cost](benchmark_runtime_vs_cost.png)\n\n")
        f.write(
            "![Top-1 vs Runtime (colored by Cost)](benchmark_top1_vs_runtime_cost.png)\n\n"
        )
        f.write("## Table of Results\n\n")
        f.write("| r | alpha | dropout | top-1 | MRR | runtime (s) | cost (USD) |\n")
        f.write("|---|-------|---------|-------|-----|-------------|------------|\n")
        if not filtered:
            f.write("| No valid results found |\n")
        else:
            for r in filtered:
                f.write(
                    f"| {r['hyperparams'].get('r', '')} "
                    f"| {r['hyperparams'].get('alpha', '')} "
                    f"| {r['hyperparams'].get('dropout', '')} "
                    f"| {safe_fmt(r['peft_retrieval'].get('top1'))} "
                    f"| {safe_fmt(r['peft_retrieval'].get('mrr'))} "
                    f"| {safe_fmt(r.get('timing_seconds'))} "
                    f"| {safe_fmt(r.get('estimated_cost_usd'))} |\n"
                )
    logging.info(f"Markdown benchmark report saved to {md_path}")


def main():
    setup_logging()
    visualize_benchmarks()


if __name__ == "__main__":
    main()
