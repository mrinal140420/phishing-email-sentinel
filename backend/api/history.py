from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional

from backend.db.mongodb import MongoDBClient

router = APIRouter(prefix="/api", tags=["history"])
db_client = None


def init_db():
    """Initialize database client."""
    global db_client
    try:
        db_client = MongoDBClient()
    except Exception as e:
        print(f"Warning: MongoDB not available: {str(e)}")
        db_client = None


@router.get("/history")
async def get_history(
    domain: Optional[str] = Query(None),
    verdict: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0)
) -> Dict[str, Any]:
    """
    Get scan history.

    Args:
        domain (Optional[str]): Filter by sender domain.
        verdict (Optional[str]): Filter by verdict (PHISHING/BENIGN).
        limit (int): Maximum results to return.
        offset (int): Number of results to skip.

    Returns:
        Dict[str, Any]: Scan history.
    """
    if not db_client:
        raise HTTPException(status_code=503, detail="Database not available")

    results = db_client.query_history(domain, verdict, limit, offset)

    return {
        "count": len(results),
        "results": results
    }


@router.get("/history/stats")
async def get_stats() -> Dict[str, Any]:
    """
    Get scan statistics.

    Returns:
        Dict[str, Any]: Statistics.
    """
    if not db_client:
        raise HTTPException(status_code=503, detail="Database not available")

    try:
        total = db_client.collection.count_documents({})
        phishing = db_client.collection.count_documents({"verdict": "PHISHING"})
        benign = db_client.collection.count_documents({"verdict": "BENIGN"})

        return {
            "total_scans": total,
            "phishing_detected": phishing,
            "benign": benign
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")