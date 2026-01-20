from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from datetime import datetime


class ScanResultSchema(BaseModel):
    """
    Schema for storing scan results in MongoDB.
    """
    scan_id: str
    sender_domain: str
    verdict: str  # "PHISHING" or "BENIGN"
    confidence: float
    signals: Dict[str, Any]
    created_at: str  # ISO-8601 timestamp

    class Config:
        schema_extra = {
            "example": {
                "scan_id": "550e8400-e29b-41d4-a716-446655440000",
                "sender_domain": "example.com",
                "verdict": "PHISHING",
                "confidence": 0.75,
                "signals": {
                    "rules": ["urgent_subject", "suspicious_phrases"],
                    "ml_probability": 0.7
                },
                "created_at": "2026-01-19T16:22:30.693186"
            }
        }


class ScanHistoryQuerySchema(BaseModel):
    """
    Schema for querying scan history.
    """
    domain: Optional[str] = None
    verdict: Optional[str] = None
    limit: int = 100
    offset: int = 0