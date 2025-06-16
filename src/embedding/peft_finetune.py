from peft import get_peft_model, LoraConfig, TaskType
from transformers import AutoModel, AutoTokenizer, TrainingArguments, Trainer
import torch
import json
import yaml
from typing import List, Optional

def train_peft_lora(
    base_model_name: str,
    train_texts: list,
    train_labels: list,
    output_dir: str = "peft_adapter",
    r: int = 8,
    alpha: int = 32,
    dropout: float = 0.1,
    num_train_epochs: int = 1,
    batch_size: int = 8
):
    # Load base model and tokenizer
    model = AutoModel.from_pretrained(base_model_name)
    tokenizer = AutoTokenizer.from_pretrained(base_model_name)

    # Prepare PEFT config
    peft_config = LoraConfig(
        task_type=TaskType.FEATURE_EXTRACTION,
        r=r,
        lora_alpha=alpha,
        lora_dropout=dropout
    )

    # Wrap model with PEFT
    peft_model = get_peft_model(model, peft_config)

    # Prepare dataset (dummy example)
    class DummyDataset(torch.utils.data.Dataset):
        def __init__(self, texts):
            self.texts = texts
        def __len__(self):
            return len(self.texts)
        def __getitem__(self, idx):
            return {
                "input_ids": tokenizer(self.texts[idx], return_tensors="pt", truncation=True, padding="max_length", max_length=128)["input_ids"].squeeze()
            }

    train_dataset = DummyDataset(train_texts)

    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=batch_size,
        num_train_epochs=num_train_epochs,
        logging_steps=10,
        save_steps=10,
        save_total_limit=1,
        remove_unused_columns=False,
        report_to="none"
    )

    # Trainer
    trainer = Trainer(
        model=peft_model,
        args=training_args,
        train_dataset=train_dataset
    )

    trainer.train()
    peft_model.save_pretrained(output_dir)
    print(f"PEFT adapter saved to {output_dir}")

def load_training_texts_and_labels(supervised: bool = False) -> (List[str], Optional[List[int]]):
    """
    Loads cleaned code and documentation chunks from your pipeline outputs.
    If supervised=True, expects each entry to have a 'label' field.
    Returns a list of text strings and, if supervised, a list of labels.
    """
    data_files = [
        "data/clean/github_repos.json",
        "data/clean/docs.json"
    ]
    texts = []
    labels = []
    for file in data_files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for entry in data:
                    if isinstance(entry, dict) and "content" in entry:
                        texts.append(entry["content"])
                        if supervised:
                            labels.append(entry.get("label", 0))  # Default to 0 if label missing
                    elif isinstance(entry, str):
                        texts.append(entry)
                        if supervised:
                            labels.append(0)
        except Exception as e:
            print(f"Warning: Could not load {file}: {e}")
    if supervised:
        return texts, labels
    return texts, None

def load_config(config_path="config.yaml"):
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    config = load_config("config.yaml")
    supervised = config.get("peft", {}).get("supervised", False)
    if supervised:
        train_texts, train_labels = load_training_texts_and_labels(supervised=True)
    else:
        train_texts, _ = load_training_texts_and_labels(supervised=False)
        train_labels = [0] * len(train_texts)  # Dummy labels for unsupervised

    peft_cfg = config.get("peft", {})
    embedding_cfg = config.get("embedding", {})
    paths_cfg = config.get("paths", {})

    train_peft_lora(
        base_model_name=embedding_cfg.get("model_name", "sentence-transformers/all-MiniLM-L6-v2"),
        train_texts=train_texts,
        train_labels=train_labels,
        output_dir=peft_cfg.get("output_dir", paths_cfg.get("peft_adapter", "peft_adapter")),
        r=peft_cfg.get("r", 8),
        alpha=peft_cfg.get("alpha", 32),
        dropout=peft_cfg.get("dropout", 0.1),
        num_train_epochs=peft_cfg.get("num_train_epochs", 1),
        batch_size=peft_cfg.get("batch_size", 8)
    )

if __name__ == "__main__":
    main()