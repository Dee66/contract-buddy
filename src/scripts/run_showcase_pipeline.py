import os
import sys
import subprocess
from src.utils.environment import setup_logging
import yaml

def check_json_file(path, min_len, desc):
    import json
    import logging
    if not os.path.exists(path):
        logging.error(f"{desc} at {path} does not exist.")
        return False
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Support both old (list) and new (dict with "runs") formats
    if isinstance(data, dict) and "runs" in data:
        entries = data["runs"]
    else:
        entries = data
    if not isinstance(entries, list) or len(entries) < min_len:
        logging.error(f"{desc} at {path} is invalid or has fewer than {min_len} entries.")
        return False
    logging.info(f"Validated {desc}: {len(entries)} entries.")
    return True

def run_step(cmd, desc):
    logging = __import__("logging")
    logging.info(f"Starting: {desc}")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        if result.stdout:
            logging.debug(f"{desc} output:\n{result.stdout}")
        if result.stderr:
            logging.debug(f"{desc} errors:\n{result.stderr}")
        logging.info(f"{desc} completed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"{desc} failed with exit code {e.returncode}")
        if e.stdout:
            logging.error(f"Stdout:\n{e.stdout}")
        if e.stderr:
            logging.error(f"Stderr:\n{e.stderr}")
        sys.exit(1)

def print_summary():
    results_path = "data/clean/hyperparam_sweep_results.json"
    logging = __import__("logging")
    if os.path.exists(results_path):
        with open(results_path, "r", encoding="utf-8") as f:
            results = json.load(f)
        if results:
            best = max(
                results,
                key=lambda r: (
                    r.get("peft_retrieval", {}).get("top1", float('-inf'))
                    if isinstance(r.get("peft_retrieval", {}).get("top1"), (int, float))
                    else float('-inf')
                )
            )
            logging.info(f"Total runs: {len(results)}")
            logging.info(
                f"Best top-1: {best['peft_retrieval'].get('top1')} "
                f"(hyperparams: {best['hyperparams']})"
            )
        else:
            logging.info("No results found for summary statistics.")

def log_file_status(path, desc):
    import os
    logging = __import__("logging")
    if os.path.exists(path):
        size = os.path.getsize(path)
        logging.info(f"{desc}: {path} exists, size={size} bytes")
    else:
        logging.warning(f"{desc}: {path} does NOT exist")

def load_and_set_env(config_path="config.yaml"):
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    env = config.get("environment", "dev")
    os.environ["MODE"] = env  # For legacy code
    os.environ["CB_ENV"] = env  # For new code

def load_config(path="config.yaml"):
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    env = config.get("environment", "dev")
    env_config = config.get(env, {})
    return env, env_config

def main():
    setup_logging()
    load_and_set_env()  # Ensure environment is set for all subprocesses
    logging = __import__("logging")
    logging.info("=== Pre-flight Check: Contract Buddy Showcase Pipeline ===")

    # Load environment-specific config
    env, env_config = load_config()
    logging.info(f"Loaded configuration for environment: {env}")

    # Step 1: Generate docstrings
    run_step([sys.executable, "-m", "src.scripts.generate_python_docstrings_dataset"], "Generate Python docstrings dataset")
    check_json_file("data/clean/docs.json", 2, "Python docstrings dataset")

    # Step 2: Download base model
    run_step([sys.executable, "-m", "src.scripts.download_base_model"], "Download base model")

    # Step 3: Prepare contrastive pairs
    run_step([sys.executable, "-m", "src.embedding.prepare_contrastive_pairs"], "Prepare contrastive pairs")
    check_json_file("data/clean/contrastive_pairs.json", 2, "Contrastive pairs for training")

    # Step 4: Run PEFT hyperparameter sweep
    run_step([sys.executable, "-m", "src.scripts.peft_hyperparam_sweep"], "Run PEFT hyperparameter sweep")
    check_json_file("data/clean/hyperparam_sweep_results.json", 1, "Aggregated hyperparameter sweep results")

    # Log file status after PEFT sweep
    log_file_status("data/clean/hyperparam_sweep_results.json", "After PEFT sweep")

    # Step 5: Analyze benchmark results
    run_step([sys.executable, "-m", "src.scripts.analyze_benchmark_results"], "Analyze benchmark results")

    # Log file status after analyze benchmark
    log_file_status("data/clean/hyperparam_sweep_results.json", "After analyze benchmark")

    # Step 6: Visualize benchmarks
    run_step([sys.executable, "-m", "src.scripts.visualize_benchmarks"], "Visualize benchmark results")

    # Log file status after visualize benchmarks
    log_file_status("data/clean/hyperparam_sweep_results.json", "After visualize benchmarks")

    # Step 6b: Generate interactive HTML report
    run_step([sys.executable, "-m", "src.scripts.generate_html_report"], "Generate interactive HTML report")

    # Log file status after generate HTML report
    log_file_status("data/clean/hyperparam_sweep_results.json", "After generate HTML report")

    # Step 7: Summarize experiments
    run_step([sys.executable, "-m", "src.scripts.summarize_experiments"], "Summarize experiments")

    # Step 8: Run all tests
    run_step([sys.executable, "run_tests.py"], "Run all tests")

    print_summary()
    logging.info("=== Pipeline complete! All pre-flight checks passed. ===")

if __name__ == "__main__":
    main()