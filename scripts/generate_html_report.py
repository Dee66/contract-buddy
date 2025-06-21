import json
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.utils.environment import get_config


def main():
    # Optionally load output path from config
    config = get_config()
    output_path = config.get("dashboard", {}).get(
        "output_path", "data/clean/benchmark_interactive.html"
    )

    with open("data/clean/hyperparam_sweep_results.json", "r", encoding="utf-8") as f:
        results = json.load(f)
    if isinstance(results, dict) and "runs" in results:
        results = results["runs"]
    df = pd.DataFrame(
        [
            {
                "r": r["hyperparams"].get("r"),
                "alpha": r["hyperparams"].get("alpha"),
                "dropout": r["hyperparams"].get("dropout"),
                "top1": r["peft_retrieval"].get("top1"),
                "mrr": r["peft_retrieval"].get("mrr"),
                "runtime": r.get("timing_seconds"),
                "cost": r.get("estimated_cost_usd"),
                "batch_size": r["hyperparams"].get("batch_size"),
            }
            for r in results
            if r.get("peft_retrieval") and r.get("estimated_cost_usd") is not None
        ]
    )

    # Main scatter plot
    fig = px.scatter(
        df,
        x="cost",
        y="top1",
        color="mrr",
        size="runtime",
        hover_data=["r", "alpha", "dropout", "batch_size", "runtime", "cost"],
        title="Top-1 Accuracy vs Cost (interactive)",
        labels={
            "cost": "Estimated Cost (USD)",
            "top1": "Top-1 Accuracy",
            "mrr": "MRR",
            "runtime": "Runtime (s)",
        },
    )

    # Add a summary table of top 5 runs by Top-1
    top5 = df.sort_values("top1", ascending=False).head(5)
    table = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=list(top5.columns), fill_color="paleturquoise", align="left"
                ),
                cells=dict(
                    values=[top5[c] for c in top5.columns],
                    fill_color="lavender",
                    align="left",
                ),
            )
        ]
    )
    table.update_layout(title="Top 5 Runs by Top-1 Accuracy")

    # Save both plots to HTML (append table below scatter)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(fig.to_html(full_html=False, include_plotlyjs="cdn"))
        f.write("<hr>")
        f.write(table.to_html(full_html=False, include_plotlyjs=False))
    print(f"Interactive HTML report saved to {output_path}")


if __name__ == "__main__":
    main()
