import torch
from peft import get_peft_model, LoraConfig, TaskType
from transformers import AutoModelForSequenceClassification, AutoTokenizer, TrainingArguments, Trainer
from typing import List, Optional
import yaml
import json

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class DummyDataset(torch.utils.data.Dataset):
    def __init__(self, texts, labels, tokenizer):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
    def __len__(self):
        return len(self.texts)
    def __getitem__(self, idx):
        return {
            "input_ids": self.tokenizer(
                self.texts[idx],
                return_tensors="pt",
                truncation=True,
                padding="max_length",
                max_length=128
            )["input_ids"].squeeze(),
            "labels": torch.tensor(self.labels[idx], dtype=torch.long)
        }

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
    model = AutoModelForSequenceClassification.from_pretrained(base_model_name, num_labels=2)
    tokenizer = AutoTokenizer.from_pretrained(base_model_name)

    # Prepare PEFT config
    peft_config = LoraConfig(
        task_type=TaskType.SEQ_CLS,
        r=r,
        lora_alpha=alpha,
        lora_dropout=dropout
    )

    # Wrap model with PEFT
    peft_model = get_peft_model(model, peft_config)
    peft_model = peft_model.to(device)

    train_dataset = DummyDataset(train_texts, train_labels, tokenizer)

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
                            labels.append(entry.get("label", 0))
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

def peft_finetune(
    pairs,
    output_dir,
    epochs,
    batch_size,
    lora_r=8,
    lora_alpha=32,
    lora_dropout=0.1,
    base_model_name="sentence-transformers/all-MiniLM-L6-v2"
):
    # Prepare texts and dummy labels
    train_texts = [p["text"] if isinstance(p, dict) and "text" in p else str(p) for p in pairs]
    train_labels = [p.get("label", 0) if isinstance(p, dict) else 0 for p in pairs]
    train_peft_lora(
        base_model_name=base_model_name,
        train_texts=train_texts,
        train_labels=train_labels,
        output_dir=output_dir,
        r=lora_r,
        alpha=lora_alpha,
        dropout=lora_dropout,
        num_train_epochs=epochs,
        batch_size=batch_size
    )

def main():
    config = load_config("config.yaml")
    supervised = config.get("peft", {}).get("supervised", False)
    if supervised:
        train_texts, train_labels = load_training_texts_and_labels(supervised=True)
    else:
        train_texts, _ = load_training_texts_and_labels(supervised=False)
        train_labels = [0] * len(train_texts)

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