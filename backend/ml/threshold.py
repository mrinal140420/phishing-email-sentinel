from typing import Literal


class ThresholdConfig:
    """
    Configuration for ML confidence thresholds.
    """
    # Probability thresholds
    HIGH_CONFIDENCE_THRESHOLD = 0.8
    MEDIUM_CONFIDENCE_THRESHOLD = 0.5
    LOW_CONFIDENCE_THRESHOLD = 0.0


def classify_confidence(probability: float) -> Literal["LOW", "MEDIUM", "HIGH"]:
    """
    Classify confidence level based on phishing probability.

    Args:
        probability (float): Phishing probability (0-1).

    Returns:
        Literal["LOW", "MEDIUM", "HIGH"]: Confidence level.
    """
    if probability >= ThresholdConfig.HIGH_CONFIDENCE_THRESHOLD:
        return "HIGH"
    elif probability >= ThresholdConfig.MEDIUM_CONFIDENCE_THRESHOLD:
        return "MEDIUM"
    else:
        return "LOW"