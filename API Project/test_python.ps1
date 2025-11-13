# Test Python Installation
Write-Host "Testing Python installation..." -ForegroundColor Cyan

# Try to find Python
$found = $false

# Check if python command works
try {
    $null = python --version 2>&1
    Write-Host "SUCCESS: python command works!" -ForegroundColor Green
    python --version
    $found = $true
} catch {
    Write-Host "python command not found" -ForegroundColor Yellow
}

# Check pip
try {
    $pipVersion = pip --version
    Write-Host "SUCCESS: pip works!" -ForegroundColor Green
    Write-Host $pipVersion
} catch {
    Write-Host "pip not found" -ForegroundColor Red
}

# Try to find Python executable
$possiblePaths = @(
    "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
    "C:\Python313\python.exe",
    "C:\Python312\python.exe"
)

Write-Host "`nSearching for Python executable..." -ForegroundColor Cyan
foreach ($path in $possiblePaths) {
    if (Test-Path $path) {
        Write-Host "FOUND: $path" -ForegroundColor Green
        & $path --version
        $found = $true
    }
}

if (-not $found) {
    Write-Host "`nPython executable not found in common locations." -ForegroundColor Red
    Write-Host "Please add Python to PATH or reinstall Python." -ForegroundColor Yellow
}
