# Assignment Setup Script for Windows
# This script helps set up the assignment environment

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "API-based Products Assignment Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python 3.7+" -ForegroundColor Red
    exit 1
}

# Check Docker installation (for Question 2)
Write-Host "Checking Docker installation..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>&1
    Write-Host "✅ Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Docker not found. Question 2 (Kong) requires Docker." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Options:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "1. Question 1 - Plagiarism Checker (Streamlit)"
Write-Host "2. Question 1 - Plagiarism Checker (Flask API)"
Write-Host "3. Question 2 - Kong API Gateway"
Write-Host "4. Question 3 - Rate Limiting Algorithms"
Write-Host "5. Setup All"
Write-Host ""

$choice = Read-Host "Enter your choice (1-5)"

switch ($choice) {
    "1" {
        Write-Host "Setting up Question 1 (Streamlit version)..." -ForegroundColor Yellow
        Set-Location plagiarism_checker
        python -m pip install -r requirements.txt
        python data_prep.py
        python model.py
        Write-Host "✅ Setup complete! Run: streamlit run app.py" -ForegroundColor Green
        Set-Location ..
    }
    "2" {
        Write-Host "Setting up Question 1 (Flask API version)..." -ForegroundColor Yellow
        Set-Location plagiarism_app
        python -m pip install -r requirements.txt
        Set-Location flask_api
        python model.py
        Set-Location ..
        Write-Host "✅ Setup complete!" -ForegroundColor Green
        Write-Host "  Terminal 1: cd flask_api && python app.py" -ForegroundColor Cyan
        Write-Host "  Terminal 2: cd streamlit_app && streamlit run app.py" -ForegroundColor Cyan
        Set-Location ..
    }
    "3" {
        Write-Host "Setting up Question 2 (Kong API Gateway)..." -ForegroundColor Yellow
        Set-Location question2_kong
        docker-compose up -d
        Write-Host "⏳ Waiting for Kong to start..." -ForegroundColor Yellow
        Start-Sleep -Seconds 30
        .\setup_kong.ps1
        Write-Host "✅ Setup complete!" -ForegroundColor Green
        Set-Location ..
    }
    "4" {
        Write-Host "Question 3 requires no setup (uses standard library only)!" -ForegroundColor Green
        Write-Host "Navigate to question3_rate_limiting and run:" -ForegroundColor Cyan
        Write-Host "  python token_bucket.py" -ForegroundColor Cyan
        Write-Host "  python leaky_bucket.py" -ForegroundColor Cyan
        Write-Host "  python comparison_demo.py" -ForegroundColor Cyan
    }
    "5" {
        Write-Host "Setting up all questions..." -ForegroundColor Yellow
        Write-Host ""
        
        # Question 1 - Streamlit
        Write-Host "[1/4] Question 1 - Streamlit version..." -ForegroundColor Cyan
        Set-Location plagiarism_checker
        python -m pip install -r requirements.txt
        python data_prep.py
        python model.py
        Set-Location ..
        
        # Question 1 - Flask
        Write-Host "[2/4] Question 1 - Flask API version..." -ForegroundColor Cyan
        Set-Location plagiarism_app
        python -m pip install -r requirements.txt
        Set-Location flask_api
        python model.py
        Set-Location ..\..
        
        # Question 2
        Write-Host "[3/4] Question 2 - Kong API Gateway..." -ForegroundColor Cyan
        Set-Location question2_kong
        docker-compose up -d
        Write-Host "⏳ Waiting for Kong..." -ForegroundColor Yellow
        Start-Sleep -Seconds 30
        .\setup_kong.ps1
        Set-Location ..
        
        # Question 3
        Write-Host "[4/4] Question 3 - Rate Limiting Algorithms..." -ForegroundColor Cyan
        Write-Host "No setup needed (standard library only)" -ForegroundColor Green
        
        Write-Host ""
        Write-Host "✅ All questions set up successfully!" -ForegroundColor Green
    }
    default {
        Write-Host "Invalid choice!" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

