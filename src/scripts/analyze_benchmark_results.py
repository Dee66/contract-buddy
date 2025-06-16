import json

def main():
    with open("data/clean/hyperparam_sweep_results.json", "r", encoding="utf-8") as f:
        results = json.load(f)

    print(f"{'r':<3} {'alpha':<5} {'dropout':<7} {'top-1':<6} {'MRR':<6} {'runtime':<8} {'mem(MB)':<8}")
    print("-" * 50)
    for res in results:
        hp = res["hyperparams"]
        print(f"{hp['r']:<3} {hp['alpha']:<5} {hp['dropout']:<7} {res.get('peft_model_top1', 0):<6.2f} {res.get('peft_model_mrr', 0):<6.2f} {res.get('train_runtime', 0):<8.2f} {res.get('net_memory_usage', 0):<8.2f}")

    # Optionally, find the best config
    best = max(results, key=lambda x: x.get("peft_model_top1", 0))
    print("\nBest config by top-1 accuracy:")
    print(best)

if __name__ == "__main__":
    main()