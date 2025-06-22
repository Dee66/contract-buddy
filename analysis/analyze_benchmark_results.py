import os
import pandas as pd
from src.adapters.environment import get_mode, setup_logging
import sys
import logging


def safe_fmt(val):
    return f"{val:.2f}" if isinstance(val, (int, float)) else "N/A"


def main():
    setup_logging()
    logging.info(f"Running benchmark analysis in {get_mode()} mode.")

    if len(sys.argv) != 3:
        logging.error(
            "Usage: python analyze_benchmark_results.py <input_dir> <output_dir>"
        )
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)

    all_results = []
    for filename in os.listdir(input_dir):
        if filename.startswith("eval_results_") and filename.endswith(".json"):
            filepath = os.path.join(input_dir, filename)
            try:
                results_df = pd.read_json(filepath, lines=True)
                all_results.append(results_df)
            except Exception as e:
                logging.warning(f"Could not process file {filename}: {e}")

    if not all_results:
        logging.warning("No evaluation results found to analyze.")
        return

    combined_df = pd.concat(all_results, ignore_index=True)

    # Basic analysis: sort by top-1 accuracy
    sorted_df = combined_df.sort_values(by="top_1_accuracy", ascending=False)

    logging.info("Top 5 performing models:")
    logging.info(sorted_df.head(5).to_string())

    # Save results
    sorted_df.to_csv(os.path.join(output_dir, "benchmark_report.csv"), index=False)
    sorted_df.to_markdown(os.path.join(output_dir, "benchmark_report.md"), index=False)

    # Save the best run for visualization
    best_run = sorted_df.iloc[0].to_dict()
    with open(os.path.join(output_dir, "best_run.json"), "w") as f:
        import json

        json.dump(best_run, f, indent=4)

    logging.info(f"Benchmark analysis complete. Reports saved to {output_dir}")


if __name__ == "__main__":
    main()
