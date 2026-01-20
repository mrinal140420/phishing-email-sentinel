# """PES – Improved Deep Learning Training Pipeline
# Binary phishing classification using CrossEncoder
# """

from google.colab import drive
drive.mount('/content/drive')

import json
import logging
from pathlib import Path

import torch
from torch.utils.data import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
)

# =========================
# Logging
# =========================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =========================
# Config (EXPLICIT DRIVE PATH)
# =========================
MODEL_NAME = "distilbert-base-uncased"

DATA_DIR = Path("/content/drive/MyDrive/data/")
MODEL_OUT_DIR = Path("/content/drive/MyDrive/pes_model/")

EPOCHS = 4
LR = 2e-5
BATCH_SIZE = 16

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
FP16 = torch.cuda.is_available()

# =========================
# Dataset
# =========================
class PhishingDataset(Dataset):
    def __init__(self, path: Path, tokenizer):
        self.samples = []
        self.tokenizer = tokenizer

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                rec = json.loads(line)
                self.samples.append((rec["text"], int(rec["label"])))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        text, label = self.samples[idx]

        encoding = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=256,
            return_tensors="pt"
        )

        return {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "labels": torch.tensor(label, dtype=torch.long)
        }

# =========================
# Training
# =========================
def train():
    logger.info(f"Device: {DEVICE}, FP16: {FP16}")

    train_path = DATA_DIR / "train.jsonl"
    if not train_path.exists():
        raise FileNotFoundError(f"Dataset not found: {train_path}")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=2
    ).to(DEVICE)

    train_ds = PhishingDataset(train_path, tokenizer)

    args = TrainingArguments(
        output_dir=str(MODEL_OUT_DIR),
        per_device_train_batch_size=BATCH_SIZE,
        num_train_epochs=EPOCHS,
        learning_rate=LR,
        weight_decay=0.01,
        fp16=FP16,
        logging_steps=50,
        save_strategy="epoch",
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_ds
    )

    logger.info("Starting training")
    trainer.train()

    MODEL_OUT_DIR.mkdir(parents=True, exist_ok=True)
    trainer.save_model(str(MODEL_OUT_DIR))
    tokenizer.save_pretrained(str(MODEL_OUT_DIR))

    logger.info("Training completed successfully")

# =========================
# Entry
# =========================
if __name__ == "__main__":
    train()