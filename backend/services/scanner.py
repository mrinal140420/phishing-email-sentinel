import uuid
from datetime import datetime
from typing import Dict, Any

from backend.core.parser import parse_email
from backend.core.rules import evaluate_rules
from backend.core.decision import make_decision
from backend.ml.model import PhishingModel


class EmailScanner:
    """
    Main scanning orchestrator: parse -> rules -> ML -> decision.
    """

    def __init__(self):
        """Initialize scanner with ML model."""
        self.model = PhishingModel()

    def scan(self, raw_email: str) -> Dict[str, Any]:
        """
        Scan an email and return phishing verdict.

        Args:
            raw_email (str): Raw RFC 822 email string.

        Returns:
            Dict[str, Any]: Scan results with verdict and signals.
        """
        scan_id = str(uuid.uuid4())

        # Step 1: Parse email
        parsed = parse_email(raw_email)
        if 'error' in parsed:
            return {
                "scan_id": scan_id,
                "verdict": "BENIGN",
                "confidence": 0.0,
                "signals": {
                    "rules": [],
                    "ml_probability": 0.0
                },
                "error": parsed['error'],
                "timestamp": datetime.now().isoformat()
            }

        # Step 2: Evaluate rules
        headers = parsed['headers']
        urls = parsed['urls']
        body = parsed['body']

        rules_output = evaluate_rules(headers, urls, body)

        # Step 3: ML inference
        email_text = f"{headers.get('subject', '')} {body.get('plain_text', '')} {body.get('html', '')}"
        ml_output = self.model.predict(email_text)

        # Step 4: Make decision
        decision = make_decision(rules_output, ml_output)

        # Extract sender domain
        sender_email = headers.get('from', '')
        sender_domain = sender_email.split('@')[-1] if '@' in sender_email else 'unknown'

        return {
            "scan_id": scan_id,
            "verdict": decision['verdict'],
            "confidence": decision['final_score'],
            "signals": {
                "rules": decision['explanation']['rules_triggered'],
                "ml_probability": ml_output.get('phishing_probability', 0.0)
            },
            "timestamp": datetime.now().isoformat()
        }