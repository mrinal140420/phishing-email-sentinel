"""
ML Model for Phishing Email Detection (DistilBERT)

- True supervised Deep Learning (fine-tuned DistilBERT)
- CPU-only inference (Render safe)
- Lazy loading
- PES contract compliant
- Robust email preprocessing (headers + HTML)
"""

from typing import Dict, Any
import logging
import re

import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from bs4 import BeautifulSoup

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

    # Strip HTML
    soup = BeautifulSoup(raw, "html.parser")
    text = soup.get_text(separator=" ")

    # Remove URLs
    text = re.sub(r"http\\S+", " ", text)

    # Normalize whitespace
    text = re.sub(r"\\s+", " ", text)

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

    def __init__(self, model_path: str = "backend/models/phishing-distilbert"):
        self.model_path = model_path
        self.device = torch.device("cpu")
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
            logger.info(f"Loading DistilBERT model from {self.model_path}")

            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_path
            )

            self.model.to(self.device)
            self.model.eval()

            self.model_loaded = True
            logger.info("✓ DistilBERT model loaded successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to load DistilBERT model: {e}")
            self.model_loaded = False
            return False

    # -------------------------
    # Inference
    # -------------------------
    def predict(self, text: str) -> Dict[str, Any]:
        if not text or not isinstance(text, str):
            return self._empty_result()

        if not self.model_loaded:
            if not self._load_model():
                return self._empty_result()

        try:
            # ✅ CLEAN INPUT (CRITICAL FIX)
            cleaned_text = clean_email_text(text)

            if not cleaned_text:
                return self._empty_result()

            inputs = self.tokenizer(
                cleaned_text,
                truncation=True,
                padding=True,
                max_length=256,
                return_tensors="pt"
            )

            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                probs = F.softmax(logits, dim=-1)

            # Class 1 = phishing
            phishing_prob = float(probs[0][1])

            # ✅ PROBABILITY FLOOR (prevents 0.0 illusion)
            phishing_prob = max(0.05, phishing_prob)

            confidence = self._confidence_level(phishing_prob)

            return {
                "model": "DistilBERT",
                "phishing_probability": round(phishing_prob, 3),
                "confidence_level": confidence
            }

        except Exception as e:
            logger.error(f"Inference error: {e}")
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
        else:
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
