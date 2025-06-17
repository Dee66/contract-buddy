import subprocess
import json
import os
import shutil

# Define hyperparameter grid
lora_rs = [4, 8]
lora_alphas = [16, 32]
lora_dropouts = [0.0, 0.1]
epochs = [1]
batch_sizes = [16]

results = []

for r in lora_rs:
    for alpha in lora_alphas:
        for dropout in lora_dropouts:
            for epoch in epochs:
                for batch_size in batch_sizes:
                    # Update config.yaml or pass as env vars/args
                    config = {
                        "embedding": {"model_name": "sentence-transformers/all-MiniLM-L6-v2"},
                        "peft": {
                            "r": r,
                            "alpha": alpha,
                            "dropout": dropout,
                            "num_train_epochs": epoch,
                            "batch_size": batch_size,
                            "output_dir": f"adapters/peft_adapter_r{r}_a{alpha}_d{dropout}_e{epoch}_b{batch_size}"
                        }
                    }
                    # Save config for this run
                    with open("config.yaml", "w") as f:
                        json.dump(config, f)
                    print(f"\nRunning PEFT fine-tuning with r={r}, alpha={alpha}, dropout={dropout}, epochs={epoch}, batch_size={batch_size}")
                    # Run fine-tuning
                    subprocess.run("python src/embedding/peft_contrastive_finetune.py", shell=True, check=True)
                    # Run evaluation with correct adapter dir
                    subprocess.run(
                        f"python src/embedding/evaluate_embeddings.py {config['peft']['output_dir']}",
                        shell=True, check=True
                    )
                    # Save results with hyperparams in filename
                    eval_path = "data/clean/eval_results.json"
                    if os.path.exists(eval_path):
                        dest = f"data/clean/eval_results_r{r}_a{alpha}_d{dropout}_e{epoch}_b{batch_size}.json"
                        shutil.copyfile(eval_path, dest)
                        with open(dest) as f:
                            res = json.load(f)
                        res["hyperparams"] = config["peft"]
                        results.append(res)

# Save all results to a summary file
with open("data/clean/hyperparam_sweep_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nHyperparameter sweep complete! See data/clean/hyperparam_sweep_results.json for all results.")