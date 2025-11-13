# Kong API Gateway Setup Script for Windows PowerShell
# This script configures Kong with rate limiting and request size limiting

Write-Host "Setting up Kong API Gateway..." -ForegroundColor Green

# Wait for Kong to be ready
Write-Host "Waiting for Kong to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Create a service for the backend
Write-Host "Creating service..." -ForegroundColor Cyan
$serviceResponse = Invoke-RestMethod -Uri "http://localhost:8001/services/" -Method POST -Body @{
    name = "backend-service"
    url = "http://backend-service:5000"
} -ContentType "application/x-www-form-urlencoded"

Write-Host "Service created: $($serviceResponse.id)" -ForegroundColor Green

# Create a route for the service
Write-Host "Creating route..." -ForegroundColor Cyan
$routeResponse = Invoke-RestMethod -Uri "http://localhost:8001/services/backend-service/routes" -Method POST -Body @{
    hosts = @("localhost")
    paths = @("/api")
} -ContentType "application/x-www-form-urlencoded"

Write-Host "Route created: $($routeResponse.id)" -ForegroundColor Green

# Enable Rate Limiting Plugin (5 requests per minute per consumer)
Write-Host "Enabling Rate Limiting plugin..." -ForegroundColor Cyan
$rateLimitResponse = Invoke-RestMethod -Uri "http://localhost:8001/services/backend-service/plugins" -Method POST -Body @{
    name = "rate-limiting"
    "config.minute" = "5"
    "config.hour" = "100"
    "config.policy" = "local"
} -ContentType "application/x-www-form-urlencoded"

Write-Host "Rate Limiting plugin enabled" -ForegroundColor Green

# Enable Request Size Limiting Plugin (1MB limit)
Write-Host "Enabling Request Size Limiting plugin..." -ForegroundColor Cyan
$sizeLimitResponse = Invoke-RestMethod -Uri "http://localhost:8001/services/backend-service/plugins" -Method POST -Body @{
    name = "request-size-limiting"
    "config.allowed_payload_size" = "1"
} -ContentType "application/x-www-form-urlencoded"

Write-Host "Request Size Limiting plugin enabled" -ForegroundColor Green

Write-Host ""
Write-Host "Kong setup completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Kong Admin API: http://localhost:8001" -ForegroundColor Yellow
Write-Host "Kong Proxy: http://localhost:8000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Test endpoints:" -ForegroundColor Cyan
Write-Host "  GET http://localhost:8000/api/" -ForegroundColor White
Write-Host "  GET http://localhost:8000/api/data" -ForegroundColor White
Write-Host "  POST http://localhost:8000/api/data" -ForegroundColor White

