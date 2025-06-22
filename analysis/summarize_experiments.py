import json
import os


def safe_fmt(val):
    return f"{val:.4f}" if isinstance(val, (int, float)) else str(val)


def main():
    exp_path = "data/clean/experiments.json"
    sweep_path = "data/clean/hyperparam_sweep_results.json"

    # If experiments.json does not exist, try to create it from sweep results
    if not os.path.exists(exp_path):
        if os.path.exists(sweep_path):
            with open(sweep_path, "r", encoding="utf-8") as f:
                sweep_results = json.load(f)
            # Wrap sweep results in a list if not already
            if isinstance(sweep_results, dict) and "runs" in sweep_results:
                sweep_results = sweep_results["runs"]
            # Convert sweep results to experiments format (minimal for test)
            experiments = []
            for i, run in enumerate(sweep_results):
                experiments.append(
                    {
                        "experiment_id": f"exp_{i}",
                        "description": f"Run {i}",
                        "timestamp": "2025-06-18 09:56",
                        "best_metrics": {
                            "top1": run.get("peft_retrieval", {}).get("top1"),
                            "mrr": run.get("peft_retrieval", {}).get("mrr"),
                            "runtime": run.get("timing_seconds"),
                            "memory_usage_mb": run.get("memory_usage_mb", 0),
                            "estimated_cost_usd": run.get("estimated_cost_usd"),
                        },
                    }
                )
            with open(exp_path, "w", encoding="utf-8") as f:
                json.dump(experiments, f, indent=2)
        else:
            print("No experiments found.")
            return

    with open(exp_path, "r", encoding="utf-8") as f:
        experiments = json.load(f)

    if not experiments:
        print("No experiments found.")
        return

    print(
        f"{'ID':<10} {'Desc':<30} {'Top-1':<8} {'MRR':<8} {'Runtime':<8} {'Mem(MB)':<8} {'Cost($)':<8} {'Timestamp':<20}"
    )
    print("-" * 100)
    for exp in experiments:
        best = exp.get("best_metrics", {})
        cost = best.get("estimated_cost_usd")
        print(
            f"{exp['experiment_id'][:8]:<10} {exp['description'][:30]:<30} "
            f"{safe_fmt(best.get('top1')):<8} {safe_fmt(best.get('mrr')):<8} "
            f"{safe_fmt(best.get('runtime')):<8} {safe_fmt(best.get('memory_usage_mb')):<8} "
            f"{safe_fmt(cost):<8} {exp['timestamp']:<20}"
        )

    # Aggregate total and average cost
    all_costs = [
        exp.get("best_metrics", {}).get("estimated_cost_usd")
        for exp in experiments
        if exp.get("best_metrics", {}).get("estimated_cost_usd") is not None
    ]
    if all_costs:
        total_cost = sum(all_costs)
        avg_cost = total_cost / len(all_costs)
        print(f"\nTotal estimated cost across all experiments: ${total_cost:.4f}")
        print(f"Average estimated cost per experiment:      ${avg_cost:.4f}")

    # Optionally, print leaderboard sorted by top-1
    print("\nLeaderboard (by Top-1):")
    leaderboard = sorted(
        experiments,
        key=lambda e: e.get("best_metrics", {}).get("top1", 0),
        reverse=True,
    )
    for i, exp in enumerate(leaderboard, 1):
        best = exp.get("best_metrics", {})
        print(
            f"{i}. {exp['experiment_id'][:8]} | Top-1: {safe_fmt(best.get('top1'))} | MRR: {safe_fmt(best.get('mrr'))} | Cost: ${safe_fmt(best.get('estimated_cost_usd'))} | {exp['description']}"
        )


if __name__ == "__main__":
    main()
