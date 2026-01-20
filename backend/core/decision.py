from typing import Dict, Any, List


def make_decision(rules_output: Dict[str, Any], ml_output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Combine rules and ML outputs to make final phishing verdict.

    Args:
        rules_output (Dict[str, Any]): Output from evaluate_rules().
        ml_output (Dict[str, Any]): Output from model.predict().

    Returns:
        Dict[str, Any]: Final decision with verdict and explanation.
    """
    # Extract scores
    rules_score = rules_output.get('rule_score', 0.0)
    ml_probability = ml_output.get('phishing_probability', 0.0)

    # Handle errors
    if 'error' in ml_output:
        ml_probability = 0.0

    # Weights for combining scores
    rules_weight = 0.4
    ml_weight = 0.6

    # Compute final score
    final_score = (rules_score * rules_weight) + (ml_probability * ml_weight)
    final_score = min(max(final_score, 0.0), 1.0)

    # Make verdict
    verdict_threshold = 0.5
    verdict = "PHISHING" if final_score >= verdict_threshold else "BENIGN"

    # Extract triggered rules for explanation
    triggered_rules = [r['rule_id'] for r in rules_output.get('triggered_rules', [])]

    return {
        "final_score": round(final_score, 3),
        "verdict": verdict,
        "explanation": {
            "rules_triggered": triggered_rules,
            "ml_weight": ml_weight,
            "rules_weight": rules_weight
        }
    }