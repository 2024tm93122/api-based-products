# API-Based Products Assignment

This repository contains the complete implementation of all three assignment questions.

## 📋 Assignment Overview

### Question 1: Plagiarism Checker API (10 marks)
Build a plagiarism detection system using Cosine Similarity and Machine Learning classification.

### Question 2: Kong API Gateway (10 marks)
Implement rate limiting and request size limiting using Kong API Gateway.

### Question 3: Rate Limiting Algorithms (10 marks)
Implement Token Bucket and Leaky Bucket rate limiting algorithms.

---

## 📁 Project Structure

```
API Project/
├── plagiarism_checker/          # Question 1: Standalone Streamlit version
│   ├── app.py
│   ├── model.py
│   ├── data_prep.py
│   ├── utils.py
│   ├── requirements.txt
│   └── sample_data/
│
├── plagiarism_app/               # Question 1: Flask API + Streamlit version
│   ├── flask_api/
│   │   ├── app.py
│   │   ├── model.py
│   │   ├── utils.py
│   │   └── requirements.txt
│   ├── streamlit_app/
│   │   ├── app.py
│   │   └── requirements.txt
│   └── sample_data/
│
├── kong_gateway/                 # Question 2: Kong API Gateway
│   ├── docker-compose.yml
│   ├── backend/
│   ├── setup_kong.sh
│   ├── setup_kong.ps1
│   ├── test_kong.py
│   └── README.md
│
├── rate_limiting/                # Question 3: Rate Limiting Algorithms
│   ├── token_bucket.py
│   ├── leaky_bucket.py
│   ├── comparison_demo.py
│   ├── api_server.py
│   ├── test_api.py
│   ├── requirements.txt
│   └── README.md
│
└── README.md                     # This file
```

---

## 🚀 Quick Start Guide

### 📖 Execution Guides

**NEW!** Detailed step-by-step guides are available:
- **[EXECUTION_GUIDE.md](EXECUTION_GUIDE.md)** - Complete step-by-step instructions for running all questions
- **[SCREENSHOT_GUIDE.md](SCREENSHOT_GUIDE.md)** - Detailed screenshot capture guide
- **[QUICK_START.md](QUICK_START.md)** - Condensed quick reference

### Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose (for Question 2)
- pip (Python package manager)

---

## ✅ Question 1: Plagiarism Checker

### Option A: Standalone Streamlit Version

```bash
cd plagiarism_checker

# Install dependencies
pip install -r requirements.txt

# Prepare training data
python data_prep.py

# Train the model
python model.py

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Option B: Flask API + Streamlit Frontend

**Terminal 1 - Start Flask API:**
```bash
cd plagiarism_app/flask_api

# Install dependencies
pip install -r requirements.txt

# Train the model (first time only)
python model.py

# Start Flask API
python app.py
```

**Terminal 2 - Start Streamlit Frontend:**
```bash
cd plagiarism_app/streamlit_app

# Install dependencies
pip install -r requirements.txt

# Start Streamlit
streamlit run app.py
```

**Features:**
- ✅ TF-IDF Vectorization
- ✅ Cosine Similarity Calculation
- ✅ ML Classification (Logistic Regression)
- ✅ Text Highlighting (matching segments)
- ✅ File Upload Interface

**Sample Data:**
- `sample_data/original.txt` - Original document
- `sample_data/submission.txt` - Submission to check

---

## ✅ Question 2: Kong API Gateway

### Setup

```bash
cd kong_gateway

# Start Kong and services
docker-compose up -d

# Wait 30 seconds for services to start, then configure Kong

# For Linux/Mac:
chmod +x setup_kong.sh
./setup_kong.sh

# For Windows (PowerShell):
.\setup_kong.ps1
```

### Testing

```bash
# Install test dependencies
pip install requests

# Run test script
python test_kong.py
```

**Manual Testing:**
```bash
# Test rate limiting (5 requests/minute)
for i in {1..7}; do
  curl http://localhost:8000/api/data
  echo ""
done

# Test request size limiting
curl -X POST http://localhost:8000/api/data \
  -H "Content-Type: application/json" \
  -d '{"data": "large payload here"}'
```

**Endpoints:**
- Kong Admin API: `http://localhost:8001`
- Kong Proxy: `http://localhost:8000`
- Backend Service: `http://localhost:5000`

**Configuration:**
- Rate Limiting: 5 requests per minute, 100 per hour
- Request Size Limit: 1MB

---

## ✅ Question 3: Rate Limiting Algorithms

### Standalone Testing

```bash
cd rate_limiting

# Install dependencies
pip install -r requirements.txt

# Test Token Bucket
python token_bucket.py

# Test Leaky Bucket
python leaky_bucket.py

# Compare both algorithms
python comparison_demo.py
```

### API Server Testing

**Terminal 1 - Start API Server:**
```bash
cd rate_limiting
python api_server.py
```

**Terminal 2 - Test API:**
```bash
cd rate_limiting
python test_api.py
```

**API Endpoints:**
- `GET /api/token-bucket` - Token Bucket rate limiting
- `GET /api/leaky-bucket` - Leaky Bucket rate limiting
- `GET /api/stats` - Get statistics
- `POST /api/reset` - Reset limiters

**Manual Testing:**
```bash
# Test Token Bucket
curl http://localhost:5001/api/token-bucket

# Test Leaky Bucket
curl http://localhost:5001/api/leaky-bucket

# Get statistics
curl http://localhost:5001/api/stats
```

**Algorithm Details:**
- **Token Bucket**: Capacity=10, Refill Rate=5/sec
- **Leaky Bucket**: Capacity=10, Leak Rate=5/sec

---

## 🔧 Troubleshooting

### Question 1 Issues:
- **Model not found**: Run `python model.py` first to train the model
- **Import errors**: Install all requirements: `pip install -r requirements.txt`

### Question 2 Issues:
- **Docker not starting**: Ensure Docker Desktop is running
- **Port conflicts**: Check if ports 8000, 8001, 5000, 5432 are available
- **Kong not ready**: Wait 30-60 seconds after `docker-compose up`

### Question 3 Issues:
- **API server not starting**: Check if port 5001 is available
- **Import errors**: Install requirements: `pip install -r requirements.txt`

---

## 📚 Technical Details

### Question 1: Technologies Used
- **Python**: Core language
- **scikit-learn**: TF-IDF, Cosine Similarity, Logistic Regression
- **Streamlit**: Web interface
- **Flask**: REST API (Option B)
- **difflib**: Text highlighting

### Question 2: Technologies Used
- **Kong API Gateway**: API gateway
- **Docker**: Containerization
- **PostgreSQL**: Kong database
- **Flask**: Backend service

### Question 3: Technologies Used
- **Python**: Core language
- **Threading**: Thread-safe implementations
- **Flask**: API server
- **Collections.deque**: Queue implementation

---

## 📝 Code Snippets for Submission

All code is well-documented and ready for submission. Key files to include in your PDF:

1. **Question 1**: `plagiarism_checker/app.py`, `plagiarism_checker/utils.py`, `plagiarism_checker/model.py`
2. **Question 2**: `kong_gateway/docker-compose.yml`, `kong_gateway/setup_kong.sh`
3. **Question 3**: `rate_limiting/token_bucket.py`, `rate_limiting/leaky_bucket.py`

---
---

For any issues or questions, refer to the individual README files in each question's directory:
- `plagiarism_checker/` - Question 1 details
- `kong_gateway/README.md` - Question 2 details
- `rate_limiting/README.md` - Question 3 details
