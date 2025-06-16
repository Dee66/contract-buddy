import subprocess
import sys
import os

def run_step(description, command):
    print(f"\n=== {description} ===")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"[ERROR] Step failed: {description}")
        sys.exit(result.returncode)

def check_data_files():
    data_files = [
        "data/clean/github_repos.json",
        "data/clean/docs.json"
    ]
    for file in data_files:
        if not os.path.exists(file):
            print(f"[ERROR] Required data file missing: {file}")
            sys.exit(1)
        with open(file, "r", encoding="utf-8") as f:
            import json
            data = json.load(f)
            if not data:
                print(f"[ERROR] Required data file is empty: {file}")
                sys.exit(1)
    print("Source data files are present and non-empty.")

def main():
    print("AI Showcase PEFT Pipeline Runner")
    check_data_files()

    run_step(
        "Preparing contrastive pairs",
        "python src/embedding/prepare_contrastive_pairs.py"
    )
    run_step(
        "Contrastive PEFT fine-tuning",
        "python src/embedding/peft_contrastive_finetune.py"
    )
    run_step(
        "Evaluating embeddings",
        "python src/embedding/evaluate_embeddings.py"
    )

    print("\nPEFT pipeline complete! Check data/clean/eval_results.json for results.")

if __name__ == "__main__":
    main()