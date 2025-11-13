# API-based Products Assignment

**Course:** SE*ZG504 - API-based Products  
**Weightage:** 30%  
**Duration:** 2 Weeks

This repository contains complete implementations for all three assignment questions.

---

## 📋 Assignment Overview

### ✅ Question 1: Plagiarism Checker API using Cosine Similarity + ML
Build a plagiarism detection system using TF-IDF vectorization, cosine similarity, and ML classification.

### ✅ Question 2: Rate Limiting and Request Size Limiting with Kong API Gateway
Configure Kong API Gateway with rate limiting and request size limiting plugins.

### ✅ Question 3: Rate Limiting Algorithms Implementation
Implement Token Bucket and Leaky Bucket rate limiting algorithms in Python.

---

## 📁 Project Structure

```
API Project/
│
├── plagiarism_checker/          # Question 1: Streamlit-only version
│   ├── app.py
│   ├── utils.py
│   ├── model.py
│   ├── data_prep.py
│   ├── requirements.txt
│   └── sample_data/
│
├── plagiarism_app/              # Question 1: Flask API + Streamlit version
│   ├── flask_api/
│   │   ├── app.py
│   │   ├── utils.py
│   │   └── model.py
│   ├── streamlit_app/
│   │   └── app.py
│   ├── requirements.txt
│   └── sample_data/
│
├── question2_kong/              # Question 2: Kong API Gateway
│   ├── docker-compose.yml
│   ├── setup_kong.sh
│   ├── setup_kong.ps1
│   ├── test_rate_limit.py
│   ├── backend/
│   └── README.md
│
├── question3_rate_limiting/    # Question 3: Rate Limiting Algorithms
│   ├── token_bucket.py
│   ├── leaky_bucket.py
│   ├── comparison_demo.py
│   └── README.md
│
└── README.md                    # This file
```

---

## 🚀 Quick Start Guide

### Question 1: Plagiarism Checker

#### Option A: Streamlit-Only Version

1. **Navigate to directory:**
   ```bash
   cd plagiarism_checker
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare training data:**
   ```bash
   python data_prep.py
   ```

4. **Train the model:**
   ```bash
   python model.py
   ```

5. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

6. **Access the app:**
   - Open browser to `http://localhost:8501`
   - Upload `sample_data/original.txt` and `sample_data/submission.txt`

#### Option B: Flask API + Streamlit Frontend

1. **Navigate to directory:**
   ```bash
   cd plagiarism_app
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Train the model (in flask_api directory):**
   ```bash
   cd flask_api
   python model.py
   cd ..
   ```

4. **Start Flask API (Terminal 1):**
   ```bash
   cd flask_api
   python app.py
   ```
   API will run on `http://localhost:5000`

5. **Start Streamlit frontend (Terminal 2):**
   ```bash
   cd streamlit_app
   streamlit run app.py
   ```
   Frontend will run on `http://localhost:8501`

### Question 2: Kong API Gateway

1. **Navigate to directory:**
   ```bash
   cd question2_kong
   ```

2. **Start Kong and services:**
   ```bash
   docker-compose up -d
   ```
   Wait ~30 seconds for services to be ready.

3. **Configure Kong:**

   **Linux/Mac:**
   ```bash
   chmod +x setup_kong.sh
   ./setup_kong.sh
   ```

   **Windows PowerShell:**
   ```powershell
   .\setup_kong.ps1
   ```

4. **Test the setup:**
   ```bash
   # Test rate limiting
   for i in {1..15}; do curl http://localhost:8000/api; echo ""; done
   
   # Or use Python test script
   pip install requests
   python test_rate_limit.py
   ```

5. **Stop services:**
   ```bash
   docker-compose down
   ```

**Configuration:**
- Rate Limit: 10 requests/minute
- Request Size Limit: 1MB
- API Endpoint: `http://localhost:8000/api`
- Admin API: `http://localhost:8001`

### Question 3: Rate Limiting Algorithms

1. **Navigate to directory:**
   ```bash
   cd question3_rate_limiting
   ```

2. **Run Token Bucket demo:**
   ```bash
   python token_bucket.py
   ```

3. **Run Leaky Bucket demo:**
   ```bash
   python leaky_bucket.py
   ```

4. **Run comparison demo:**
   ```bash
   python comparison_demo.py
   ```

**No external dependencies required** - uses only Python standard library.

---

## 📸 Screenshots Required for Assignment

### Question 1
1. Streamlit app interface showing file upload
2. Results showing similarity score and plagiarism probability
3. Highlighted matching text segments
4. Code snippets from key files (utils.py, model.py, app.py)

### Question 2
1. Kong Admin API showing services and routes
2. Kong plugins configuration (rate-limiting, request-size-limiting)
3. Rate limiting test showing 429 responses
4. Request size limiting test showing 413 responses
5. Docker containers running

### Question 3
1. Token Bucket algorithm output
2. Leaky Bucket algorithm output
3. Comparison demo output
4. Code snippets from both implementations

---

## 🔧 Technical Details

### Question 1: Technologies Used
- **Python** - Programming language
- **scikit-learn** - ML library (LogisticRegression, TfidfVectorizer)
- **Streamlit** - Web UI framework
- **Flask** - API framework (for API version)
- **pandas, numpy** - Data processing

### Question 2: Technologies Used
- **Kong API Gateway** - API gateway
- **Docker & Docker Compose** - Containerization
- **PostgreSQL** - Kong database
- **Nginx** - Backend service (for testing)

### Question 3: Technologies Used
- **Python** - Programming language
- **threading** - Thread-safe operations
- **Standard library only** - No external dependencies

---

## 📝 Assignment Submission Checklist

- [ ] Question 1: Plagiarism Checker
  - [ ] Streamlit app working
  - [ ] Model trained and saved
  - [ ] Screenshots of UI and results
  - [ ] Code snippets included

- [ ] Question 2: Kong API Gateway
  - [ ] Kong running with Docker
  - [ ] Rate limiting configured (10 req/min)
  - [ ] Request size limiting configured (1MB)
  - [ ] Screenshots of configuration and tests
  - [ ] Test results showing 429 and 413 responses

- [ ] Question 3: Rate Limiting Algorithms
  - [ ] Token Bucket implementation
  - [ ] Leaky Bucket implementation
  - [ ] Both algorithms tested and working
  - [ ] Screenshots of outputs
  - [ ] Code snippets included

---

## 🐛 Troubleshooting

### Question 1 Issues

**Model file not found:**
- Run `data_prep.py` first, then `model.py` to generate the model

**Import errors:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`

**Flask API connection error:**
- Ensure Flask API is running on port 5000
- Check firewall settings

### Question 2 Issues

**Docker containers not starting:**
- Ensure Docker is running
- Check if ports 8000, 8001, 8080 are available
- Try: `docker-compose down -v` then `docker-compose up -d`

**Kong setup script fails:**
- Wait longer for Kong to be ready (30+ seconds)
- Check Kong health: `curl http://localhost:8001/`
- Run setup commands manually (see question2_kong/README.md)

### Question 3 Issues

**No issues expected** - uses only standard library!

---

## 📚 Additional Resources

- [Kong API Gateway Documentation](https://docs.konghq.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [scikit-learn Documentation](https://scikit-learn.org/)

---

## 👤 Author

**Assignment for:** SE*ZG504 - API-based Products  
**Institution:** Birla Institute of Technology & Science, Pilani  
**Semester:** First Semester 2025-2026

---

## 📄 License

This project is created for educational purposes as part of the assignment requirements.

---

## ✅ Completion Status

- ✅ Question 1: Complete (Both versions)
- ✅ Question 2: Complete (Kong setup with rate limiting)
- ✅ Question 3: Complete (Both algorithms implemented)

**All assignment requirements have been implemented and tested!**

