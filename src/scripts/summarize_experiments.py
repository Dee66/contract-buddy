import json
import os

def safe_fmt(val):
    return f"{val:.4f}" if isinstance(val, (int, float)) else str(val)

def main():
    path = "data/clean/experiments.json"
    if not os.path.exists(path):
        print("No experiments found.")
        return

    with open(path, "r", encoding="utf-8") as f:
        experiments = json.load(f)

    if not experiments:
        print("No experiments found.")
        return

    print(f"{'ID':<10} {'Desc':<30} {'Top-1':<8} {'MRR':<8} {'Runtime':<8} {'Mem(MB)':<8} {'Cost($)':<8} {'Timestamp':<20}")
    print("-" * 100)
    for exp in experiments:
        best = exp.get("best_metrics", {})
        cost = best.get("estimated_cost_usd")
        print(f"{exp['experiment_id'][:8]:<10} {exp['description'][:30]:<30} "
              f"{safe_fmt(best.get('top1')):<8} {safe_fmt(best.get('mrr')):<8} "
              f"{safe_fmt(best.get('runtime')):<8} {safe_fmt(best.get('memory_usage_mb')):<8} "
              f"{safe_fmt(cost):<8} {exp['timestamp']:<20}")

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
    leaderboard = sorted(experiments, key=lambda e: e.get("best_metrics", {}).get("top1", 0), reverse=True)
    for i, exp in enumerate(leaderboard, 1):
        best = exp.get("best_metrics", {})
        print(f"{i}. {exp['experiment_id'][:8]} | Top-1: {safe_fmt(best.get('top1'))} | MRR: {safe_fmt(best.get('mrr'))} | Cost: ${safe_fmt(best.get('estimated_cost_usd'))} | {exp['description']}")

if __name__ == "__main__":
    main()