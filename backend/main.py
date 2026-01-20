from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# ---------------------------------
# Load .env ONLY for local dev
# (Render injects env vars automatically)
# ---------------------------------
if os.getenv("RENDER") is None:
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except Exception:
        pass

# ---------------------------------
# Routers (handle both local and Render imports)
# ---------------------------------
try:
    # Try absolute imports (Render environment)
    from backend.api import scan, history
except ImportError:
    # Fall back to relative imports (local development)
    from api import scan, history

app = FastAPI(
    title="Phishing Email Sentinel",
    description="Layered phishing email detection system",
    version="1.0.0"
)

# ---------------------------------
# CORS (open for MVP, restrict later)
# ---------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------
# MongoDB Configuration (optional)
# ---------------------------------
MONGODB_URI = os.getenv("MONGODB_URI") or os.getenv("MONGO_URI")
if not MONGODB_URI and os.getenv("RENDER"):
    print("⚠️  Warning: MONGODB_URI not set on Render. MongoDB features disabled.")

# ---------------------------------
# Initialize DB connections
# ---------------------------------
scan.init_db()
history.init_db()

# ---------------------------------
# Routes
# ---------------------------------
app.include_router(scan.router, prefix="/api", tags=["Scan"])
app.include_router(history.router, prefix="/api/history", tags=["History"])



@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "Phishing Email Sentinel"
    }


# ---------------------------------
# Local run only (Render ignores this)
# ---------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=10000,
        reload=True
    )
