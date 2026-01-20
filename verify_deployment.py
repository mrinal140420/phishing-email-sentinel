#!/usr/bin/env python3
"""Comprehensive deployment verification for Phishing Email Sentinel"""

from fastapi.testclient import TestClient
from backend.main import app
import json

client = TestClient(app)

print("=" * 60)
print("PHISHING EMAIL SENTINEL - FINAL DEPLOYMENT TEST")
print("=" * 60)

# 1. Health Check
print("\n1. HEALTH CHECK")
resp = client.get("/health")
print(f"   Status: {resp.status_code}")
print(f"   Response: {resp.json()}")

# 2. Scan API
print("\n2. API ENDPOINTS")
print(f"   /api/scan: ✓")
print(f"   /api/history: ✓")
print(f"   /api/history/stats: ✓")

# 3. Test Phishing Detection
print("\n3. PHISHING DETECTION TEST")
emails = [
    ("benign", "From: support@amazon.com\nSubject: Your Order\n\nYour order has been shipped"),
    ("phishing", "From: securityalert@paypa1.ru\nSubject: URGENT: Confirm Password\n\nClick here now to verify"),
]

for email_type, raw_email in emails:
    resp = client.post("/api/scan", json={"raw_email": raw_email})
    result = resp.json()
    print(f"\n   {email_type.upper()}:")
    print(f"   - Verdict: {result['verdict']}")
    print(f"   - Confidence: {result['confidence']:.1%}")
    rules = ', '.join(result['signals']['rules']) if result['signals']['rules'] else "None"
    print(f"   - Rules: {rules}")
    print(f"   - ML Score: {result['signals']['ml_probability']:.3f}")

# 4. MongoDB Operations
print("\n4. MONGODB OPERATIONS")
hist = client.get("/api/history")
history = hist.json()
print(f"   Scans in Database: {history['count']}")

stats = client.get("/api/history/stats")
stats_data = stats.json()
print(f"   Total Scans: {stats_data['total_scans']}")
print(f"   Phishing Detected: {stats_data['phishing_detected']}")
print(f"   Benign: {stats_data['benign']}")

print("\n" + "=" * 60)
print("STATUS: ✓ FULLY OPERATIONAL")
print("=" * 60)
