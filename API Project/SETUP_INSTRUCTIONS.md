# Setup Instructions

## Prerequisites

1. **Python 3.7+** - [Download](https://www.python.org/downloads/)
2. **Docker Desktop** (for Question 2) - [Download](https://www.docker.com/products/docker-desktop)
3. **Git** (optional) - [Download](https://git-scm.com/downloads)

## Quick Setup (Windows)

Run the PowerShell setup script:

```powershell
.\setup_assignment.ps1
```

Follow the prompts to set up individual questions or all questions at once.

## Manual Setup

### Question 1: Plagiarism Checker

#### Streamlit Version

```bash
cd plagiarism_checker
pip install -r requirements.txt
python data_prep.py
python model.py
streamlit run app.py
```

#### Flask API Version

**Terminal 1 (Flask API):**
```bash
cd plagiarism_app
pip install -r requirements.txt
cd flask_api
python model.py
python app.py
```

**Terminal 2 (Streamlit Frontend):**
```bash
cd plagiarism_app/streamlit_app
streamlit run app.py
```

### Question 2: Kong API Gateway

```bash
cd question2_kong
docker-compose up -d
# Wait 30 seconds
# Linux/Mac:
./setup_kong.sh
# Windows:
.\setup_kong.ps1
```

### Question 3: Rate Limiting Algorithms

No setup needed! Just run:

```bash
cd question3_rate_limiting
python token_bucket.py
python leaky_bucket.py
python comparison_demo.py
```

## Verification

### Question 1
- Streamlit app opens at `http://localhost:8501`
- Upload sample files and see results

### Question 2
- Kong Admin API: `http://localhost:8001`
- Test endpoint: `http://localhost:8000/api`
- Run test script: `python test_rate_limit.py`

### Question 3
- Run demos and verify output matches expected results

## Troubleshooting

See main README.md for detailed troubleshooting steps.

