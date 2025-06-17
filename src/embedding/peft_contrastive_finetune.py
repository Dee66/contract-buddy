from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
from peft import get_peft_model, LoraConfig, TaskType
import json
import os
import yaml

def load_pairs(path="data/clean/contrastive_pairs.json"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Pairs file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        pairs = json.load(f)
    if not pairs:
        raise ValueError(f"No pairs found in {path}. Run prepare_contrastive_pairs.py and check data.")
    return [InputExample(texts=[a, b]) for a, b in pairs]

def load_config(config_path="config.yaml"):
    if not os.path.exists(config_path):
        print("No config.yaml found, using defaults.")
        return {}
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    config = load_config("config.yaml")
    model_name = config.get("embedding", {}).get("model_name", "sentence-transformers/all-MiniLM-L6-v2")
    lora_cfg = config.get("peft", {})
    lora_r = lora_cfg.get("r", 8)
    lora_alpha = lora_cfg.get("alpha", 32)
    lora_dropout = lora_cfg.get("dropout", 0.1)
    batch_size = lora_cfg.get("batch_size", 16)
    epochs = lora_cfg.get("num_train_epochs", 1)
    output_dir = lora_cfg.get("output_dir", "peft_adapter_contrastive")

    model = SentenceTransformer(model_name)
    transformer = model[0].auto_model
    peft_config = LoraConfig(
        task_type=TaskType.FEATURE_EXTRACTION,
        r=lora_r,
        lora_alpha=lora_alpha,
        lora_dropout=lora_dropout
    )
    transformer = get_peft_model(transformer, peft_config)
    model[0].auto_model = transformer

    train_examples = load_pairs()
    if not train_examples:
        raise ValueError("No training pairs found. Please check data.")
    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=batch_size)
    train_loss = losses.MultipleNegativesRankingLoss(model)

    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=epochs,
        warmup_steps=10,
        output_path=output_dir
    )
    print(f"PEFT contrastive adapter saved to {output_dir}")

if __name__ == "__main__":
    main()