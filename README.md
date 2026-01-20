# Phishing Email Sentinel (PES)

A deployable, CPU-only, layered phishing email detection system using fine-tuned DistilBERT and rule-based detection. Designed for free and open-source deployment.

## Overview

PES is a comprehensive phishing email detection system that combines **rule-based detection** with **machine learning** (fine-tuned DistilBERT) to identify phishing emails with high accuracy. The architecture follows a layered approach: rules first for fast detection, ML for complex patterns.

## Architecture

```
Frontend (React) 
    ↓
Backend (FastAPI) 
    ├─→ Rules Engine (pattern matching)
    ├─→ ML Module (DistilBERT - CPU-only)
    ├─→ HTML Sanitizer
    ├─→ Email Parser
    └─→ MongoDB (metadata & history)
```

### Core Components

- **Frontend**: React SPA with email upload and scan history visualization
- **Backend**: FastAPI REST API with layered detection pipeline
- **Database**: MongoDB Atlas (free tier) for metadata and scan history
- **ML Model**: Fine-tuned DistilBERT for phishing classification (CPU-only inference)
- **Deployment**: Docker + Docker Compose for containerized deployment
- **Rules Engine**: Pattern-based detection with configurable thresholds

## Key Features

- ✅ **Layered Detection**: Rules-based first (fast), ML second (comprehensive)
- ✅ **Advanced ML**: Fine-tuned DistilBERT model for deep learning-based detection
- ✅ **CPU-Only**: No GPU required - deployable on free cloud tiers
- ✅ **HTML Sanitization**: Safe parsing of email content
- ✅ **Email Parsing**: RFC 822 compliant email parsing
- ✅ **Scan History**: Persistent storage of detection results
- ✅ **RESTful API**: FastAPI with automatic API documentation
- ✅ **No Raw Storage**: Metadata-only approach for privacy
- ✅ **Docker Ready**: Easy deployment with Docker Compose
- ✅ **Open Source**: Built with free and open-source tools

## Model Repository

**Hugging Face Model**: [Elite1038/pes-distilbert-phishing](https://huggingface.co/Elite1038/pes-distilbert-phishing)

The fine-tuned DistilBERT model is hosted on Hugging Face Hub and automatically downloaded on first run:

```python
from huggingface_hub import login, upload_folder

# Login with Hugging Face credentials (if needed)
login()

# Push model files to repository
upload_folder(
    folder_path="./backend/models/phishing-distilbert",
    repo_id="Elite1038/pes-distilbert-phishing",
    repo_type="model"
)
```

**Model Details**:
- **Architecture**: DistilBERT (distilled BERT)
- **Training**: Fine-tuned on phishing vs. legitimate emails
- **Size**: Lightweight, CPU-compatible
- **Tokenizer**: HuggingFace compatible
- **Auto-Download**: Model cached after first use

## Capacities & Detection Mechanisms

### Rule-Based Detection
The rules engine evaluates multiple phishing indicators:
- **Suspicious Sender Domains**: Detects high-risk TLDs (ru, cn, tk, ml, ga, cf)
- **Urgent Subject Keywords**: Identifies action-oriented language (verify, confirm, urgent, immediate)
- **Multiple Domain URLs**: Detects emails with URLs from different domains
- **Spoofed Reply-To Headers**: Identifies mismatches between sender and reply-to
- **Suspicious URL Patterns**: Detects obfuscated and deceptive URLs
- **Attachment Risks**: Flags potentially dangerous file types
- **HTML/CSS Tricks**: Identifies deceptive HTML formatting

### Machine Learning Detection (DistilBERT)
- **Fine-tuned Model**: DistilBERT specifically trained for phishing classification
- **Email Content Analysis**: Analyzes headers, subject, and body content
- **HTML Preprocessing**: Safely extracts and processes HTML email content
- **Confidence Scoring**: Provides probability scores for predictions
- **CPU-Optimized**: Lightweight model suitable for free cloud deployment

### Combined Decision Engine
- **Weighted Scoring**: Combines rule scores with ML confidence
- **Configurable Thresholds**: Adjustable risk thresholds for different use cases
- **Detailed Reasoning**: Provides explanation for each detection
- **Audit Trail**: Stores complete detection history

## Project Modules

### Backend Core Modules

| Module | Path | Responsibility |
|--------|------|---|
| **Parser** | `backend/core/parser.py` | RFC 822 email parsing into structured data |
| **Rules Engine** | `backend/core/rules.py` | Rule-based phishing detection scoring |
| **Sanitizer** | `backend/core/sanitizer.py` | Safe HTML content sanitization |
| **Decision Engine** | `backend/core/decision.py` | Combines rules + ML for final verdict |

### Backend ML Modules

| Module | Path | Responsibility |
|--------|------|---|
| **Model** | `backend/ml/model.py` | DistilBERT fine-tuned phishing classifier (CPU inference) |
| **Vectorizer** | `backend/ml/vectorizer.py` | Text vectorization and preprocessing |
| **Threshold** | `backend/ml/threshold.py` | Dynamic threshold management |

### Backend Services & APIs

| Module | Path | Responsibility |
|--------|------|---|
| **Scanner Service** | `backend/services/scanner.py` | Orchestrates full detection pipeline |
| **Scan API** | `backend/api/scan.py` | `/scan` endpoint for email analysis |
| **History API** | `backend/api/history.py` | `/history` endpoint for scan records |

### Backend Database

| Module | Path | Responsibility |
|--------|------|---|
| **MongoDB Handler** | `backend/db/mongodb.py` | Database connection and operations |
| **Schemas** | `backend/db/schemas.py` | Pydantic schemas for data validation |

### Frontend Components

| Component | Path | Purpose |
|-----------|------|---------|
| **Upload Page** | `frontend/pages/Upload.jsx` | Email file upload and scan interface |
| **History Page** | `frontend/pages/History.jsx` | Scan history and statistics dashboard |
| **FileUploader** | `frontend/components/FileUploader.jsx` | Reusable file upload component |
| **ResultCard** | `frontend/components/ResultCard.jsx` | Display and format scan results |
| **API Service** | `frontend/services/api.js` | Backend API client |

### ML Training & Evaluation

| Script | Path | Purpose |
|--------|------|---------|
| **Train Script** | `ml/train.py` | Fine-tune DistilBERT on phishing dataset |
| **Evaluate Script** | `ml/evaluate.py` | Evaluate model performance |
| **Dataset Preparation** | `ml/data/scripts/prepare_dataset.py` | Prepare training data |

## Data Specifications

### Supported Email Format
- **RFC 822 Format**: Standard email format (.eml files)
- **Multipart Support**: Handles complex email structures
- **HTML & Plain Text**: Processes both email content types

### Training Dataset
- **Location**: `ml/data/`
- **Processed Data**: `train.jsonl`, `val.jsonl`, `test.jsonl`
- **Raw Data**: `ham.csv`, `phishing.csv`
- **Categories**: Binary classification (phishing vs. legitimate)

## Setup & Installation

### Prerequisites

- **Python**: 3.11 or higher
- **Node.js**: 18 or higher
- **MongoDB Atlas**: Free tier account
- **Docker** (optional): For containerized deployment
- **Git**: For version control

### Environment Configuration

Create a `.env` file in the root directory:

```bash
# MongoDB Configuration
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/pes_db?retryWrites=true&w=majority
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/pes_db?retryWrites=true&w=majority

# Optional: HuggingFace Model Repository
HF_MODEL_REPO=Elite1038/pes-distilbert-phishing

# Optional: Render deployment
RENDER=false
```

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Download ML model** (on first run, automatically fetched from HuggingFace)

4. **Run backend server**
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000
API documentation: http://localhost:8000/docs

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start development server**
```bash
npm start
```

Frontend will be available at: http://localhost:3000

### Docker Deployment

1. **Build and run with Docker Compose**
```bash
docker-compose up --build
```

2. **Access services**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

3. **Stop services**
```bash
docker-compose down
```

## API Endpoints

### Scan Endpoint
```
POST /scan
Content-Type: multipart/form-data

Body:
  - file: [email.eml] (required)

Response:
{
  "filename": "email.eml",
  "is_phishing": boolean,
  "confidence": float (0.0-1.0),
  "rules_score": float,
  "ml_score": float,
  "triggered_rules": [...],
  "reasoning": string,
  "timestamp": ISO8601
}
```

### History Endpoint
```
GET /history?limit=50&skip=0

Response:
{
  "total": integer,
  "scans": [
    {
      "id": string,
      "filename": string,
      "is_phishing": boolean,
      "confidence": float,
      "timestamp": ISO8601,
      "sender": string,
      "subject": string
    }
  ]
}
```

## Testing

Run the test scripts to verify functionality:

```bash
# Test API endpoints
python test_api.py

# Test ML model
python test_model.py

# Test full pipeline
python test_pipeline.py

# Verify deployment
python verify_deployment.py
```

## Performance Characteristics

- **Email Processing**: < 2 seconds per email
- **Model Inference**: CPU-optimized (DistilBERT)
- **Memory Footprint**: ~500MB for full stack
- **Accuracy**: Achieved through rule + ML combination
- **Scalability**: Supports batch processing with Docker Compose

## Deployment Status

Check deployment documentation:
- [Deployment Status](DEPLOYMENT_STATUS.md)
- [Implementation Report](IMPLEMENTATION_REPORT.md)
- [Render Deployment Guide](RENDER_DEPLOYMENT.md)
- [Model Implementation](MODEL_IMPLEMENTATION.md)

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

## Technology Stack

### Backend
- **Framework**: FastAPI (Python web framework)
- **Async Runtime**: Uvicorn ASGI server
- **ML Framework**: PyTorch + Hugging Face Transformers
- **NLP Model**: DistilBERT (fine-tuned for phishing)
- **Database**: MongoDB with PyMongo
- **HTML Processing**: BeautifulSoup + lxml
- **Email Validation**: email-validator
- **Data Validation**: Pydantic

### Frontend
- **UI Framework**: React 18.2
- **HTTP Client**: Axios
- **Build Tool**: React Scripts
- **Styling**: CSS

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Deployment**: Render (free tier compatible)
- **Database Service**: MongoDB Atlas (free tier)
- **Model Repository**: Hugging Face Hub

## Project Structure Summary

```
mini-c/
├── backend/              # FastAPI backend
│   ├── core/            # Detection engines
│   ├── ml/              # Machine learning modules
│   ├── api/             # API endpoints
│   ├── db/              # Database layer
│   ├── services/        # Business logic
│   ├── models/          # Pre-trained models
│   └── main.py          # FastAPI app entry
├── frontend/            # React frontend
│   ├── src/            # Source code
│   ├── pages/          # Page components
│   ├── components/     # Reusable components
│   ├── services/       # API clients
│   └── public/         # Static assets
├── ml/                 # ML training & evaluation
│   ├── data/          # Datasets
│   ├── train.py       # Training script
│   └── evaluate.py    # Evaluation script
├── infra/             # Infrastructure configs
│   └── docker-compose.yml
└── [test files]       # Testing utilities
```

## Troubleshooting

### Common Issues

**Issue**: Model fails to download
- **Solution**: Ensure internet connection for first run, model is cached after initial download

**Issue**: MongoDB connection error
- **Solution**: Verify MONGODB_URI in .env file, check MongoDB Atlas IP whitelist

**Issue**: Frontend can't connect to backend
- **Solution**: Ensure backend is running on port 8000, check CORS headers

**Issue**: Slow email processing
- **Solution**: This is normal on CPU - process emails sequentially or increase timeout values

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Performance Metrics

- **Phishing Detection Rate**: High accuracy from combined rule + ML approach
- **False Positive Rate**: Low due to conservative threshold settings
- **Average Processing Time**: 1-2 seconds per email
- **Memory Usage**: ~500MB for full stack
- **CPU Usage**: Single-threaded processing, suitable for free cloud tiers

## Documentation Files

- [README.md](README.md) - This file
- [DEPLOYMENT_STATUS.md](DEPLOYMENT_STATUS.md) - Current deployment status
- [IMPLEMENTATION_REPORT.md](IMPLEMENTATION_REPORT.md) - Detailed implementation notes
- [MODEL_STATUS.md](MODEL_STATUS.md) - Model training and performance status
- [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) - Render platform deployment guide
- [RENDER_FIX_SUMMARY.md](RENDER_FIX_SUMMARY.md) - Fixes and improvements summary

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
1. Check existing [Documentation Files](#documentation-files)
2. Review test files for usage examples
3. Check FastAPI auto-documentation at `/docs` endpoint
