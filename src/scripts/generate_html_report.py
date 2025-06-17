import json
import plotly.express as px
import pandas as pd

def main():
    with open("data/clean/hyperparam_sweep_results.json", "r", encoding="utf-8") as f:
        results = json.load(f)
    if isinstance(results, dict) and "runs" in results:
        results = results["runs"]
    df = pd.DataFrame([
        {
            "r": r["hyperparams"].get("r"),
            "alpha": r["hyperparams"].get("alpha"),
            "dropout": r["hyperparams"].get("dropout"),
            "top1": r["peft_retrieval"].get("top1"),
            "mrr": r["peft_retrieval"].get("mrr"),
            "runtime": r.get("timing_seconds"),
            "cost": r.get("estimated_cost_usd"),
        }
        for r in results
        if r.get("peft_retrieval") and r.get("estimated_cost_usd") is not None
    ])
    fig = px.scatter(
        df, x="cost", y="top1", color="mrr",
        hover_data=["r", "alpha", "dropout", "runtime"],
        title="Top-1 Accuracy vs Cost (interactive)"
    )
    fig.write_html("data/clean/benchmark_interactive.html")
    print("Interactive HTML report saved to data/clean/benchmark_interactive.html")

if __name__ == "__main__":
    main()