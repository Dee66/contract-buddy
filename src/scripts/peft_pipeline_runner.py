from src.utils.environment import get_mode, setup_logging
from src.embedding.peft_finetune import peft_finetune
from src.embedding.evaluate_embeddings import evaluate_model
from src.embedding.prepare_contrastive_pairs import prepare_contrastive_pairs

def main():
    setup_logging()
    mode = get_mode()
    logging = __import__("logging")
    logging.info(f"PEFT pipeline running in {mode.upper()} mode")

    # DEV mode: use smaller dataset, fewer epochs, smaller batch size
    if mode == "dev":
        train_pairs_path = "data/clean/contrastive_pairs.json"
        model_output_dir = "adapters/peft_adapter_dev"
        epochs = 1
        batch_size = 8
        max_pairs = 50  # Only use 50 pairs for quick dev runs
        logging.info("DEV mode: Using 50 pairs, 1 epoch, batch size 8")
    else:
        train_pairs_path = "data/clean/contrastive_pairs.json"
        model_output_dir = "adapters/peft_adapter_prod"
        epochs = 3
        batch_size = 32
        max_pairs = None  # Use all pairs
        logging.info("PROD mode: Using all pairs, 3 epochs, batch size 32")

    # Prepare contrastive pairs (if needed)
    pairs = prepare_contrastive_pairs(train_pairs_path)
    if max_pairs:
        pairs = pairs[:max_pairs]

    # Fine-tune with PEFT
    peft_finetune(
        pairs=pairs,
        output_dir=model_output_dir,
        epochs=epochs,
        batch_size=batch_size
    )

    # Evaluate the fine-tuned model
    evaluate_model(
        model_dir=model_output_dir,
        eval_data_path="data/clean/docs.json"
    )

    logging.info("PEFT pipeline completed successfully.")

if __name__ == "__main__":
    setup_logging()
    mode = get_mode()
    logging = __import__("logging")
    logging.info(f"PEFT pipeline runner started in {mode.upper()} mode")
    main()