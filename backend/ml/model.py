"""
ML Model for Phishing Email Detection (DistilBERT)

- True supervised Deep Learning (fine-tuned DistilBERT)
- CPU-only inference (Render safe)
- Lazy loading
- HuggingFace repo based (single source of truth)
- Robust email preprocessing (headers + HTML)
- PES contract compliant
"""

from typing import Dict, Any
import os
import logging
import re

import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from bs4 import BeautifulSoup

# =========================
# Config
# =========================
MODEL_REPO = os.getenv(
    "HF_MODEL_REPO",
    "Elite1038/pes-distilbert-phishing"
)

DEVICE = torch.device("cpu")

logger = logging.getLogger(__name__)


# =========================
# Email Preprocessing
# =========================
def clean_email_text(raw: str) -> str:
    """
    Cleans raw email input for ML inference.

    Steps:
    1. Strip headers
    2. Remove HTML markup
    3. Remove URLs
    4. Normalize whitespace
    """
    if not isinstance(raw, str):
        return ""

    # Remove headers (everything before first empty line)
    if "\n\n" in raw:
        raw = raw.split("\n\n", 1)[1]

    # Strip HTML safely
    soup = BeautifulSoup(raw, "html.parser")
    text = soup.get_text(separator=" ")

    # Remove URLs
    text = re.sub(r"http\S+", " ", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================
# Model Wrapper
# =========================
class PhishingModel:
    """
    DistilBERT-based phishing detection model.

    Contract Output:
    {
        "model": "DistilBERT",
        "phishing_probability": float (0-1),
        "confidence_level": "LOW" | "MEDIUM" | "HIGH"
    }
    """

    def __init__(self):
        self.device = DEVICE
        self.model = None
        self.tokenizer = None
        self.model_loaded = False

    # -------------------------
    # Lazy Load Model
    # -------------------------
    def _load_model(self) -> bool:
        if self.model_loaded:
            return True

        try:
            logger.info(f"Loading DistilBERT from HuggingFace: {MODEL_REPO}")

            self.tokenizer = AutoTokenizer.from_pretrained(MODEL_REPO)
            self.model = AutoModelForSequenceClassification.from_pretrained(
                MODEL_REPO
            )

            self.model.to(self.device)
            self.model.eval()

            self.model_loaded = True
            logger.info("✓ DistilBERT model loaded successfully")
            return True

        except Exception as e:
            logger.exception("❌ Failed to load DistilBERT model")
            self.model_loaded = False
            return False

    # -------------------------
    # Inference
    # -------------------------
    def predict(self, raw_email: str) -> Dict[str, Any]:
        if not raw_email or not isinstance(raw_email, str):
            return self._empty_result()

        if not self.model_loaded and not self._load_model():
            return self._empty_result()

        cleaned_text = clean_email_text(raw_email)
        if not cleaned_text:
            return self._empty_result()

        try:
            inputs = self.tokenizer(
                cleaned_text,
                truncation=True,
                padding=True,
                max_length=256,
                return_tensors="pt"
            )

            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            with torch.no_grad():
                logits = self.model(**inputs).logits
                probs = F.softmax(logits, dim=-1)

            # Class index 1 = phishing
            phishing_prob = float(probs[0][1])

            # Probability floor (prevents false certainty)
            phishing_prob = max(0.05, phishing_prob)

            return {
                "model": "DistilBERT",
                "phishing_probability": round(phishing_prob, 3),
                "confidence_level": self._confidence_level(phishing_prob)
            }

        except Exception:
            logger.exception("❌ Inference failure")
            return self._empty_result()

    # -------------------------
    # Confidence Mapping
    # -------------------------
    @staticmethod
    def _confidence_level(prob: float) -> str:
        if prob >= 0.80:
            return "HIGH"
        elif prob >= 0.50:
            return "MEDIUM"
        return "LOW"

    # -------------------------
    # Safe Default
    # -------------------------
    @staticmethod
    def _empty_result() -> Dict[str, Any]:
        return {
            "model": "DistilBERT",
            "phishing_probability": 0.05,
            "confidence_level": "LOW"
        }
