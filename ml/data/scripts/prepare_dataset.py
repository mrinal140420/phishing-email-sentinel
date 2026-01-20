"""
Dataset preparation script for Phishing Email Sentinel (PES)

Sources:
- phishing.csv → labeled phishing emails (uses 'body', 'label')
- ham.csv → benign emails (uses 'message')

Output:
- train.jsonl
- val.jsonl
- test.jsonl
"""

import json
import random
import re
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

RAW_DIR = Path("ml/data/raw")
OUT_DIR = Path("ml/data/processed")

RANDOM_SEED = 42
MAX_SAMPLES_PER_CLASS = 40000  # balance dataset


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"http\\S+", " ", text)
    text = re.sub(r"\\s+", " ", text)
    return text.strip()


def load_phishing():
    """Load phishing emails from phishing.csv"""
    df = pd.read_csv(RAW_DIR / "phishing.csv")

    records = []
    for _, row in df.iterrows():
        text = clean_text(row["body"])
        label = int(row["label"])

        if len(text) < 30:
            continue

        records.append({
            "text": text,
            "label": label
        })

    return records


def load_ham():
    """Load benign emails from ham.csv"""
    df = pd.read_csv(RAW_DIR / "ham.csv")

    records = []
    for _, row in df.iterrows():
        text = clean_text(row["message"])

        if len(text) < 30:
            continue

        records.append({
            "text": text,
            "label": 0
        })

    return records


def write_jsonl(data, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for row in data:
            f.write(json.dumps(row) + "\n")


def main():
    random.seed(RANDOM_SEED)

    phishing = load_phishing()
    ham = load_ham()

    random.shuffle(phishing)
    random.shuffle(ham)

    phishing = phishing[:MAX_SAMPLES_PER_CLASS]
    ham = ham[:MAX_SAMPLES_PER_CLASS]

    data = phishing + ham
    random.shuffle(data)

    train, temp = train_test_split(
        data,
        test_size=0.3,
        random_state=RANDOM_SEED,
        stratify=[d["label"] for d in data]
    )

    val, test = train_test_split(
        temp,
        test_size=0.5,
        random_state=RANDOM_SEED,
        stratify=[d["label"] for d in temp]
    )

    write_jsonl(train, OUT_DIR / "train.jsonl")
    write_jsonl(val, OUT_DIR / "val.jsonl")
    write_jsonl(test, OUT_DIR / "test.jsonl")

    print("Dataset created successfully:")
    print(f"Train: {len(train)}")
    print(f"Val:   {len(val)}")
    print(f"Test:  {len(test)}")


if __name__ == "__main__":
    main()
