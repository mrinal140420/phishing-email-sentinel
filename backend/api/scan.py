from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from services.scanner import EmailScanner
from db.mongodb import MongoDBClient
from db.schemas import ScanResultSchema

router = APIRouter(prefix="/api", tags=["scan"])
scanner = EmailScanner()
db_client = None


def init_db():
    """Initialize database client."""
    global db_client
    try:
        db_client = MongoDBClient()
    except Exception as e:
        print(f"Warning: MongoDB not available: {str(e)}")
        db_client = None


class ScanRequest(BaseModel):
    """Request schema for scan endpoint."""
    raw_email: str


class ScanResponse(BaseModel):
    """Response schema for scan endpoint."""
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


@router.post("/scan", response_model=ScanResponse)
async def scan_email(request: ScanRequest) -> Dict[str, Any]:
    """
    Scan an email for phishing.

    Args:
        request (ScanRequest): Email to scan.

    Returns:
        Dict[str, Any]: Scan results.
    """
    if not request.raw_email:
        raise HTTPException(status_code=400, detail="raw_email cannot be empty")

    # Scan email
    result = scanner.scan(request.raw_email)

    # Try to store in database
    if db_client:
        try:
            db_result = {
                "scan_id": result['scan_id'],
                "sender_domain": "unknown",
                "verdict": result['verdict'],
                "confidence": result['confidence'],
                "signals": result['signals'],
                "created_at": result['timestamp']
            }
            db_client.insert_scan_result(db_result)
        except Exception as e:
            print(f"Warning: Failed to store result: {str(e)}")

    return {
        "scan_id": result['scan_id'],
        "verdict": result['verdict'],
        "confidence": result['confidence'],
        "signals": result['signals']
    }


@router.post("/scan/file")
async def scan_email_file(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Scan an email from uploaded file.

    Args:
        file (UploadFile): EML file to scan.

    Returns:
        Dict[str, Any]: Scan results.
    """
    try:
        content = await file.read()
        raw_email = content.decode('utf-8', errors='ignore')
        result = scanner.scan(raw_email)

        # Try to store in database
        if db_client:
            try:
                db_result = {
                    "scan_id": result['scan_id'],
                    "sender_domain": "unknown",
                    "verdict": result['verdict'],
                    "confidence": result['confidence'],
                    "signals": result['signals'],
                    "created_at": result['timestamp']
                }
                db_client.insert_scan_result(db_result)
            except Exception as e:
                print(f"Warning: Failed to store result: {str(e)}")

        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process file: {str(e)}")