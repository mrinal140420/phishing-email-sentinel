from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from services.scanner import EmailScanner
from db.mongodb import MongoDBClient

router = APIRouter(tags=["scan"])
scanner = EmailScanner()
db_client = None


# =========================
# DB INIT (NOT A ROUTE)
# =========================
def init_db():
    """Initialize database client."""
    global db_client
    try:
        db_client = MongoDBClient()
    except Exception as e:
        print(f"Warning: MongoDB not available: {str(e)}")
        db_client = None


# =========================
# Schemas
# =========================
class ScanRequest(BaseModel):
    raw_email: str


class ScanResponse(BaseModel):
    scan_id: str
    verdict: str
    confidence: float
    signals: Dict[str, Any]

    class Config:
        json_schema_extra = {
            "example": {
                "scan_id": "550e8400-e29b-41d4-a716-446655440000",
                "verdict": "PHISHING",
                "confidence": 0.85,
                "signals": {
                    "rules": ["urgent_subject"],
                    "ml_probability": 0.8
                }
            }
        }


# =========================
# Routes
# =========================
@router.post("/scan", response_model=ScanResponse)
async def scan_email(request: ScanRequest) -> Dict[str, Any]:
    if not request.raw_email:
        raise HTTPException(status_code=400, detail="raw_email cannot be empty")

    result = scanner.scan(request.raw_email)

    if db_client:
        try:
            db_client.insert_scan_result({
                "scan_id": result["scan_id"],
                "sender_domain": "unknown",
                "verdict": result["verdict"],
                "confidence": result["confidence"],
                "signals": result["signals"],
                "created_at": result["timestamp"]
            })
        except Exception as e:
            print(f"Warning: Failed to store result: {str(e)}")

    return {
        "scan_id": result["scan_id"],
        "verdict": result["verdict"],
        "confidence": result["confidence"],
        "signals": result["signals"]
    }


@router.post("/scan/file", response_model=ScanResponse)
async def scan_email_file(file: UploadFile = File(...)) -> Dict[str, Any]:
    try:
        content = await file.read()
        raw_email = content.decode("utf-8", errors="ignore")

        result = scanner.scan(raw_email)

        if db_client:
            try:
                db_client.insert_scan_result({
                    "scan_id": result["scan_id"],
                    "sender_domain": "unknown",
                    "verdict": result["verdict"],
                    "confidence": result["confidence"],
                    "signals": result["signals"],
                    "created_at": result["timestamp"]
                })
            except Exception as e:
                print(f"Warning: Failed to store result: {str(e)}")

        return {
            "scan_id": result["scan_id"],
            "verdict": result["verdict"],
            "confidence": result["confidence"],
            "signals": result["signals"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to process file: {str(e)}"
        )
