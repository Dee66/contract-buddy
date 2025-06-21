from src.utils.environment import get_mode, setup_logging, get_env_config
from src.embedding.peft_finetune import peft_finetune
from src.embedding.evaluate_embeddings import evaluate_model
from src.embedding.prepare_contrastive_pairs import prepare_contrastive_pairs
import yaml


def load_config(path="src/scripts/config.yaml"):
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    env = config.get("environment", "dev")
    env_config = config.get(env, {})
    return env, env_config


def main():
    setup_logging()
    mode = get_mode()
    logging = __import__("logging")
    logging.info(f"PEFT pipeline running in {mode.upper()} mode")

    env_config = get_env_config()
    dataset_size = env_config.get("dataset_size", 100)
    sweep_params = env_config.get("sweep_params", {})
    epochs = sweep_params.get("epochs", [1])[0]
    batch_size = sweep_params.get("batch_sizes", [8])[0]
    max_pairs = dataset_size

    train_pairs_path = "data/clean/contrastive_pairs.json"
    model_output_dir = f"adapters/peft_adapter_{mode}"

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
    setup_logging()
    mode = get_mode()
    logging = __import__("logging")
    logging.info(f"PEFT pipeline runner started in {mode.upper()} mode")
    main()
