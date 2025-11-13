# Kong API Gateway Setup Script for Windows PowerShell
# This script configures Kong with rate limiting and request size limiting

Write-Host "🚀 Setting up Kong API Gateway..." -ForegroundColor Green

# Wait for Kong to be ready
Write-Host "⏳ Waiting for Kong to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Create a service
Write-Host "📦 Creating service..." -ForegroundColor Cyan
$serviceResponse = Invoke-RestMethod -Uri "http://localhost:8001/services/" -Method POST -Body @{
    name = "backend-service"
    url = "http://backend-service:80"
} -ContentType "application/x-www-form-urlencoded"

Write-Host "Service created: $($serviceResponse.id)" -ForegroundColor Green

# Create a route
Write-Host "🛣️  Creating route..." -ForegroundColor Cyan
$routeResponse = Invoke-RestMethod -Uri "http://localhost:8001/services/backend-service/routes" -Method POST -Body @{
    hosts = @("localhost")
    paths = @("/api")
} -ContentType "application/x-www-form-urlencoded"

Write-Host "Route created: $($routeResponse.id)" -ForegroundColor Green

# Enable Rate Limiting Plugin (10 requests per minute)
Write-Host "⏱️  Enabling Rate Limiting (10 requests/minute)..." -ForegroundColor Cyan
$rateLimitResponse = Invoke-RestMethod -Uri "http://localhost:8001/services/backend-service/plugins" -Method POST -Body @{
    name = "rate-limiting"
    "config.minute" = 10
    "config.hour" = 100
    "config.policy" = "local"
} -ContentType "application/x-www-form-urlencoded"

Write-Host "Rate limiting enabled: $($rateLimitResponse.id)" -ForegroundColor Green

# Enable Request Size Limiting Plugin (1MB)
Write-Host "📏 Enabling Request Size Limiting (1MB)..." -ForegroundColor Cyan
$sizeLimitResponse = Invoke-RestMethod -Uri "http://localhost:8001/services/backend-service/plugins" -Method POST -Body @{
    name = "request-size-limiting"
    "config.allowed_payload_size" = 1
} -ContentType "application/x-www-form-urlencoded"

Write-Host "Request size limiting enabled: $($sizeLimitResponse.id)" -ForegroundColor Green

Write-Host ""
Write-Host "✅ Kong setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Summary:" -ForegroundColor Yellow
Write-Host "  - Service: backend-service"
Write-Host "  - Route: http://localhost:8000/api"
Write-Host "  - Rate Limit: 10 requests/minute"
Write-Host "  - Request Size Limit: 1MB"
Write-Host ""
Write-Host "🧪 Test the setup:" -ForegroundColor Cyan
Write-Host "  Invoke-WebRequest -Uri http://localhost:8000/api"

