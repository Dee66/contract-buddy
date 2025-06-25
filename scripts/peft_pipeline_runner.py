import os
import sys
import logging

# 🟦 NOTE: Ensure src is on the Python path for all environments (dev, staging, prod)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Use canonical config and logging setup for the whole repo
from src.adapters.environment import setup_logging, get_mode, ConfigLoader
from src.adapters.embedding.peft_finetune import peft_finetune
from src.adapters.embedding.evaluate_embeddings import evaluate_model
from src.adapters.embedding.prepare_contrastive_pairs import prepare_contrastive_pairs


def main():
    setup_logging()
    mode = get_mode()
    logging.info(f"PEFT pipeline running in {mode.upper()} mode")

    config = ConfigLoader().get_config()
    dataset_size = getattr(config, "rag_pipeline", None)
    if dataset_size is not None:
        dataset_size = getattr(config.rag_pipeline, "dataset_size", 100)
    else:
        dataset_size = 100
    sweep_params = getattr(config.rag_pipeline, "sweep_params", {})
    epochs = sweep_params.get("epochs", [1])[0]
    batch_size = sweep_params.get("batch_sizes", [8])[0]
    max_pairs = dataset_size

    train_pairs_path = "data/clean/contrastive_pairs.json"
    model_output_dir = f"artifacts/adapters/peft_adapter_{mode}"

    logging.info(
        f"{mode.upper()} mode: Using {max_pairs or 'all'} pairs, {epochs} epoch(s), batch size {batch_size}"
    )

    pairs = prepare_contrastive_pairs(train_pairs_path)
    if max_pairs:
        pairs = pairs[:max_pairs]

    peft_finetune(
        pairs=pairs, output_dir=model_output_dir, epochs=epochs, batch_size=batch_size
    )

    evaluate_model(model_dir=model_output_dir, eval_data_path="data/clean/docs.json")

    logging.info("PEFT pipeline completed successfully.")


if __name__ == "__main__":
    main()
