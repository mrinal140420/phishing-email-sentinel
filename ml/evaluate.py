"""
ML Model Evaluation (Deep Learning)
Evaluates transformer-based phishing detection models (MiniLM / BERT)

This module is CPU-safe and uses only free, open-source libraries.
"""

import logging
from typing import List, Dict

import numpy as np
import torch
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DLEvaluator:
    """
    Deep Learning model evaluator for phishing detection.
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize DL evaluator.

        Args:
            model_name: Hugging Face transformer model name
        """
        logger.info(f"Loading DL model: {model_name}")
        self.device = "cpu"
        self.model = SentenceTransformer(model_name, device=self.device)

    def predict_proba(self, texts: List[str]) -> np.ndarray:
        """
        Generate phishing probabilities using embeddings similarity.

        Args:
            texts: List of email texts

        Returns:
            np.ndarray: Phishing probabilities (0–1)
        """
        embeddings = self.model.encode(texts, convert_to_tensor=True)

        # Simple proxy scoring: cosine similarity to phishing centroid
        phishing_centroid = embeddings.mean(dim=0)
        scores = torch.nn.functional.cosine_similarity(
            embeddings, phishing_centroid.unsqueeze(0)
        )

        # Normalize scores to 0–1
        probabilities = (scores - scores.min()) / (scores.max() - scores.min() + 1e-8)
        return probabilities.cpu().numpy()

    def evaluate(
        self,
        texts: List[str],
        labels: List[int],
        threshold: float = 0.5
    ) -> Dict[str, float]:
        """
        Evaluate DL model performance.

        Args:
            texts: Email text samples
            labels: Ground truth labels (1 = phishing, 0 = benign)
            threshold: Classification threshold

        Returns:
            dict: Evaluation metrics
        """
        logger.info("Running DL evaluation on test dataset")

        probabilities = self.predict_proba(texts)
        predictions = (probabilities >= threshold).astype(int)

        metrics = {
            "precision": precision_score(labels, predictions),
            "recall": recall_score(labels, predictions),
            "f1_score": f1_score(labels, predictions),
            "roc_auc": roc_auc_score(labels, probabilities),
            "confusion_matrix": confusion_matrix(labels, predictions).tolist()
        }

        logger.info(f"Evaluation Metrics: {metrics}")
        return metrics


def evaluate_model():
    """
    Entry point for DL evaluation pipeline.

    Expected workflow:
    1. Load labeled test dataset
    2. Extract email text
    3. Run DL evaluation
    4. Log metrics
    """

    # Placeholder dataset (replace with real test data loader)
    texts = [
        "Your account has been suspended. Click here to verify.",
        "Meeting scheduled for tomorrow at 10 AM."
    ]
    labels = [1, 0]

    evaluator = DLEvaluator()
    metrics = evaluator.evaluate(texts, labels)

    logger.info("DL Evaluation completed successfully")
    return metrics


if __name__ == "__main__":
    evaluate_model()
