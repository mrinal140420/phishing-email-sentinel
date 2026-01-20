from typing import List


def vectorize_text(text: str, model) -> List[float]:
    """
    Vectorize text using the ML model's encoder.

    Args:
        text (str): Text to vectorize.
        model: The ML model instance with encode method.

    Returns:
        List[float]: Embedding vector.
    """
    if not text:
        # Return zero vector for empty text
        return [0.0] * 384  # MiniLM output dimension

    try:
        embedding = model.encode(text)
        return embedding.tolist()
    except Exception as e:
        raise ValueError(f"Failed to vectorize text: {str(e)}")