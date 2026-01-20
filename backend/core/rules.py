import re
from typing import Dict, List, Any


def evaluate_rules(headers: Dict[str, Any], urls: List[Dict[str, str]], body: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate rules-based phishing detection on parsed email data.

    Args:
        headers (Dict[str, Any]): Email headers.
        urls (List[Dict[str, str]]): List of URLs with domains.
        body (Dict[str, Any]): Email body content.

    Returns:
        Dict[str, Any]: Rule evaluation results.
    """
    triggered_rules = []
    total_score = 0.0

    # Rule 1: Suspicious sender domain
    sender = headers.get('from', '').lower()
    if re.search(r'@.*\.(ru|cn|tk|ml|ga|cf)$', sender):
        triggered_rules.append({
            "rule_id": "suspicious_sender_domain",
            "description": "Sender domain is from a suspicious TLD",
            "weight": 0.3
        })
        total_score += 0.3

    # Rule 2: Subject contains urgent keywords
    subject = headers.get('subject', '').lower()
    urgent_keywords = ['urgent', 'immediate', 'action required', 'verify', 'confirm']
    if any(keyword in subject for keyword in urgent_keywords):
        triggered_rules.append({
            "rule_id": "urgent_subject",
            "description": "Subject contains urgent or action-oriented keywords",
            "weight": 0.2
        })
        total_score += 0.2

    # Rule 3: Multiple URLs from different domains
    domains = set(url['domain'] for url in urls if url['domain'])
    if len(domains) > 1:
        triggered_rules.append({
            "rule_id": "multiple_domains",
            "description": "Email contains URLs from multiple different domains",
            "weight": 0.25
        })
        total_score += 0.25

    # Rule 4: URLs not matching sender domain
    sender_domain = sender.split('@')[-1] if '@' in sender else ''
    if sender_domain and any(url['domain'] != sender_domain for url in urls):
        triggered_rules.append({
            "rule_id": "url_mismatch",
            "description": "URLs point to domains different from sender domain",
            "weight": 0.15
        })
        total_score += 0.15

    # Rule 5: Body contains suspicious phrases
    body_text = (body.get('plain_text', '') or '') + ' ' + (body.get('html', '') or '')
    body_text = body_text.lower()
    suspicious_phrases = ['click here', 'login now', 'update your information', 'account suspended']
    if any(phrase in body_text for phrase in suspicious_phrases):
        triggered_rules.append({
            "rule_id": "suspicious_phrases",
            "description": "Body contains common phishing phrases",
            "weight": 0.1
        })
        total_score += 0.1

    # Cap score at 1.0
    rule_score = min(total_score, 1.0)

    return {
        "rule_score": rule_score,
        "triggered_rules": triggered_rules
    }