import asyncio
from backend.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

# Test health
resp = client.get("/health")
print("Health check:", resp.json())

# Test scan with benign email
resp = client.post("/api/scan", json={
    "raw_email": "From: admin@example.com\nSubject: Meeting Tomorrow\n\nLet's meet at 10am"
})
print("\nBenign email scan:", resp.json())

# Test scan with phishing email
resp = client.post("/api/scan", json={
    "raw_email": "From: attacker@phishing.ru\nSubject: URGENT Action Required\n\nClick here now to verify your account!"
})
print("\nPhishing email scan:", resp.json())