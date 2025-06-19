from src.utils.environment import get_mode, setup_logging
from src.embedding.peft_finetune import peft_finetune
from src.embedding.evaluate_embeddings import generate_negative_pairs, retrieval_metrics
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from peft import PeftModel
from transformers import logging as hf_logging
import json
import os
import sys
import psutil
import warnings
import uuid
import platform
import subprocess
import random
import time

hf_logging.set_verbosity_error()
warnings.filterwarnings("ignore", category=UserWarning)

def get_git_hash():
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
    except Exception:
        return "unknown"

def update_experiment_index(experiment_meta, results_path, best_metrics):
    index_path = "data/clean/experiments.json"
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            index = json.load(f)
    else:
        index = []
    entry = {
        "experiment_id": experiment_meta["experiment_id"],
        "description": experiment_meta["description"],
        "timestamp": experiment_meta["timestamp"],
        "results_path": results_path,
        "best_metrics": best_metrics
    }
    index.append(entry)
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

def get_env_info():
    return dict(os.environ)

def get_package_versions():
    import transformers, torch, peft
    return {
        "transformers": transformers.__version__,
        "torch": torch.__version__,
        "peft": peft.__version__,
    }

def get_gpu_info():
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        if gpus:
            return {
                "gpu_name": gpus[0].name,
                "gpu_load": gpus[0].load,
                "gpu_memory_total": gpus[0].memoryTotal,
                "gpu_memory_used": gpus[0].memoryUsed,
            }
    except ImportError:
        pass
    return {}

def estimate_local_cost(runtime_seconds, cpu_percent, gpu_load=None, mode="prod"):
    # These are rough estimates based on cloud pricing (USD/hour)
    CPU_COST_PER_HOUR = 0.05 if mode == "dev" else 0.20  # dev: local, prod: cloud-like
    GPU_COST_PER_HOUR = 0.0 if mode == "dev" else 1.00   # dev: assume no GPU, prod: cloud GPU

    cpu_hours = (runtime_seconds / 3600.0) * (cpu_percent / 100.0)
    cpu_cost = cpu_hours * CPU_COST_PER_HOUR

    gpu_cost = 0.0
    if gpu_load is not None and gpu_load > 0:
        gpu_hours = (runtime_seconds / 3600.0) * gpu_load
        gpu_cost = gpu_hours * GPU_COST_PER_HOUR

    return round(cpu_cost + gpu_cost, 4)

def get_cloud_info():
    # Example for AWS EC2 or similar cloud environment
    instance_type = os.environ.get("EC2_INSTANCE_TYPE", "local")
    hourly_rate = float(os.environ.get("CLOUD_HOURLY_RATE", "0.0"))
    return {
        "instance_type": instance_type,
        "hourly_rate_usd": hourly_rate
    }

def main():
    setup_logging()
    logging = __import__("logging")
    mode = get_mode()
    logging.info(f"PEFT hyperparameter sweep running in {mode.upper()} mode")

    env_config = get_env_config()
    sweep_params = env_config.get("sweep_params", {})
    lora_rs = sweep_params.get("lora_rs", [4])
    lora_alphas = sweep_params.get("lora_alphas", [16])
    lora_dropouts = sweep_params.get("lora_dropouts", [0.0])
    epochs = sweep_params.get("epochs", [1])
    batch_sizes = sweep_params.get("batch_sizes", [8])
    max_pairs = env_config.get("dataset_size", None)
    logging.info(f"{mode.upper()} mode: {max_pairs or 'all'} pairs, epochs {epochs}, batch sizes {batch_sizes}")

    input_path = "data/clean/contrastive_pairs.json"
    output_path = "data/clean/hyperparam_sweep_results.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if not os.path.exists(input_path):
        logging.error(f"Input file missing: {input_path}")
        sys.exit(1)

    # Load pairs
    with open(input_path, "r", encoding="utf-8") as f:
        pairs = json.load(f)
    if max_pairs:
        pairs = pairs[:max_pairs]
        logging.info(f"Using first {max_pairs} pairs.")

    if len(pairs) < 2:
        logging.error("Not enough pairs to run sweep. Please add more data to data/clean/contrastive_pairs.json.")
        sys.exit(1)

    experiment_id = str(uuid.uuid4())
    experiment_description = "PEFT sweep on baseline dataset"
    experiment_timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")
    dataset_version = "v1"  # update as needed
    code_version = get_git_hash()
    random_seed = 42
    random.seed(random_seed)

    experiment_meta = {
        "experiment_id": experiment_id,
        "description": experiment_description,
        "timestamp": experiment_timestamp,
        "dataset_version": dataset_version,
        "code_version": code_version,
        "random_seed": random_seed,
        "system": platform.platform(),
        "python_version": platform.python_version(),
    }
    experiment_meta["env"] = get_env_info()
    experiment_meta["package_versions"] = get_package_versions()
    experiment_meta["gpu_info"] = get_gpu_info()
    experiment_meta["cloud_info"] = get_cloud_info()

    all_results = []
    best_run_metrics = None  # Initialize best_run_metrics
    for r in lora_rs:
        for alpha in lora_alphas:
            for dropout in lora_dropouts:
                for epoch in epochs:
                    for batch_size in batch_sizes:
                        output_dir = f"adapters/peft_adapter_r{r}_a{alpha}_d{dropout}_e{epoch}_b{batch_size}"
                        logging.info(f"Running PEFT finetune: r={r}, alpha={alpha}, dropout={dropout}, epochs={epoch}, batch_size={batch_size}")
                        peft_finetune(
                            pairs=pairs,
                            output_dir=output_dir,
                            epochs=epoch,
                            batch_size=batch_size,
                            lora_r=r,
                            lora_alpha=alpha,
                            lora_dropout=dropout
                        )
                        base_model_name = "sentence-transformers/all-MiniLM-L6-v2"
                        tokenizer = AutoTokenizer.from_pretrained(base_model_name)
                        base_model = AutoModelForSequenceClassification.from_pretrained(base_model_name)
                        model = PeftModel.from_pretrained(base_model, output_dir)

                        logging.info("Classifier head weights are randomly initialized. This is expected and handled by fine-tuning.")
                        logging.info("label_names is set to [] as this is an embedding task, not classification.")

                        # Evaluate and ensure real metrics are returned
                        start_time = time.time()
                        process = psutil.Process(os.getpid())
                        negatives = generate_negative_pairs(pairs)
                        try:
                            metrics = retrieval_metrics(model, pairs, negatives, tokenizer=tokenizer)
                        except Exception as e:
                            logging.error(f"retrieval_metrics failed for r={r}, alpha={alpha}, dropout={dropout}, epochs={epoch}, batch_size={batch_size}: {e}")
                            metrics = {"top1": None, "topk": None, "mrr": None}
                        timing_seconds = time.time() - start_time
                        memory_usage_mb = process.memory_info().rss / 1024 / 1024

                        cpu_percent = psutil.cpu_percent()
                        mem = psutil.virtual_memory()
                        run_resource = {
                            "cpu_percent": cpu_percent,
                            "memory_used_mb": mem.used / (1024 * 1024),
                        }
                        run_resource.update(get_gpu_info())

                        cost = estimate_local_cost(
                            runtime_seconds=timing_seconds,
                            cpu_percent=cpu_percent,
                            gpu_load=run_resource.get("gpu_load", None),
                            mode=mode
                        )

                        all_results.append({
                            "hyperparams": {
                                "r": r,
                                "alpha": alpha,
                                "dropout": dropout,
                                "epochs": epoch,
                                "batch_size": batch_size
                            },
                            "peft_retrieval": metrics,
                            "timing_seconds": timing_seconds,
                            "memory_usage_mb": memory_usage_mb,
                            "resource": run_resource,
                            "estimated_cost_usd": cost
                        })

                        # Update best_run_metrics based on some criteria, e.g., highest top1 accuracy
                        if best_run_metrics is None or metrics["top1"] > best_run_metrics["top1"]:
                            best_run_metrics = metrics

    # Save results
    os.makedirs("data/clean", exist_ok=True)
    output = {
        "experiment": experiment_meta,
        "runs": all_results
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    logging.info(f"PEFT hyperparameter sweep completed and results saved. {len(all_results)} results written.")
    logging.info(f"File exists after write: {os.path.exists(output_path)}")

    # Update experiment index
    update_experiment_index(
        experiment_meta,
        "data/clean/hyperparam_sweep_results.json",
        best_metrics=best_run_metrics  # set this to best run's metrics
    )

if __name__ == "__main__":
    main()
