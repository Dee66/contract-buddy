import subprocess
import sys
import os

def run(cmd, desc):
    print(f"\n=== {desc} ===")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"[ERROR] Step failed: {desc}")
        sys.exit(result.returncode)

def main():
    # All paths are relative to project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
    os.chdir(project_root)

    # Step 1: Download base model
    run("python src/scripts/download_base_model.py", "Downloading and caching base model")
    # Step 2: Prepare contrastive pairs
    run("python src/embedding/prepare_contrastive_pairs.py", "Preparing contrastive pairs")
    # Step 3: Run PEFT hyperparameter sweep
    run("python src/scripts/peft_hyperparam_sweep.py", "Running PEFT hyperparameter sweep")
    # Step 4: (Optional) Run all tests
    run("python run_tests.py", "Running all tests")
    # Generate Python docstrings dataset
    subprocess.run("python src/scripts/generate_python_docstrings_dataset.py", shell=True, check=True)
    print("\nShowcase pipeline complete! See data/clean/hyperparam_sweep_results.json for results.")

if __name__ == "__main__":
    main()
    main()