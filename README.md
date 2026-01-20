# Phishing Email Sentinel (PES)

A deployable, CPU-only, layered phishing email detection system using free and open-source tools.

## Overview

PES combines rule-based detection with machine learning (MiniLM) to identify phishing emails. The architecture follows a layered approach: rules first for fast detection, ML for complex patterns.

## Architecture

```
Frontend (React) → Backend (FastAPI) → ML Module (MiniLM) + Rules Engine
                                    ↓
                            MongoDB Atlas (Free)
```

### Components

- **Frontend**: React SPA with email upload and scan history
- **Backend**: FastAPI with layered detection pipeline
- **Database**: MongoDB Atlas free tier (metadata only)
- **ML**: sentence-transformers MiniLM (CPU-only inference)
- **Deployment**: Docker + Docker Compose

## Features

- ✅ Layered detection: Rules-based first, ML last
- ✅ No raw email storage (metadata only)
- ✅ HTML sanitization
- ✅ CPU-only inference
- ✅ Free and open-source
- ✅ Docker deployable

## Modules

### Backend

| Module | Responsibility |
|--------|---|
| `parser.py` | Parse RFC 822 emails into structured data |
| `rules.py` | Rule-based phishing detection |
| `sanitizer.py` | HTML content sanitization |
| `model.py` | MiniLM inference |
| `decision.py` | Combine rules + ML for final verdict |
| `scanner.py` | Orchestrate full pipeline |
| `api/scan.py` | Scan API endpoint |
| `api/history.py` | History API endpoint |
| `db/mongodb.py` | MongoDB connection handler |
| `db/schemas.py` | Data schemas |

### Frontend

| Component | Purpose |
|-----------|---------|
| `Upload.jsx` | Email upload and scan interface |
| `History.jsx` | Scan history and statistics |
| `FileUploader.jsx` | File upload component |
| `ResultCard.jsx` | Display scan results |

## Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB Atlas free account
- Docker (optional)

### Environment Variables

```bash
# .env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/pes_db?retryWrites=true&w=majority
```

### Local Development

1. **Backend**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

2. **Frontend**
```bash
cd frontend
npm install
npm start
```

### Docker Deployment

```bash
docker-compose up --build
```

Backend: http://localhost:8000
Frontend: http://localhost:3000

## API Endpoints

### POST /api/scan
Scan an email for phishing.

**Request:**
```json
{
  "raw_email": "From: attacker@phishing.com\nSubject: Urgent Action\n\nClick here"
}
```

**Response:**
```json
{
  "scan_id": "uuid",
  "verdict": "PHISHING",
  "confidence": 0.85,
  "signals": {
    "rules": ["urgent_subject", "suspicious_phrases"],
    "ml_probability": 0.8
  }
}
```

### GET /api/history
Get scan history with optional filters.

**Query Parameters:**
- `domain`: Filter by sender domain
- `verdict`: Filter by verdict (PHISHING/BENIGN)
- `limit`: Max results (default 100)
- `offset`: Pagination offset (default 0)

### GET /api/history/stats
Get scan statistics.

**Response:**
```json
{
  "total_scans": 150,
  "phishing_detected": 45,
  "benign": 105
}
```

## Detection Rules

1. **Suspicious Sender Domain** (0.3 weight)
   - TLDs: .ru, .cn, .tk, .ml, .ga, .cf

2. **Urgent Subject** (0.2 weight)
   - Keywords: urgent, immediate, action required, verify, confirm

3. **Multiple Domains** (0.25 weight)
   - Email contains URLs from multiple different domains

4. **URL Mismatch** (0.15 weight)
   - URLs point to domains different from sender domain

5. **Suspicious Phrases** (0.1 weight)
   - Phrases: click here, login now, update your information, account suspended

## ML Model

- **Model**: sentence-transformers/all-MiniLM-L6-v2
- **Inference**: CPU-only
- **Embedding Dimension**: 384
- **Size**: ~80MB

## Database Schema

### scan_results Collection

```json
{
  "scan_id": "uuid",
  "sender_domain": "example.com",
  "verdict": "PHISHING|BENIGN",
  "confidence": 0.85,
  "signals": {
    "rules": ["rule1", "rule2"],
    "ml_probability": 0.8
  },
  "created_at": "2026-01-19T16:22:30Z"
}
```

**Indexes:**
- `created_at`: For time-based queries
- `verdict`: For filtering

## Performance

- Average scan time: 200-500ms (CPU dependent)
- Memory usage: ~200-300MB (model loaded)
- Database: Free tier supports unlimited metadata

## License

MIT