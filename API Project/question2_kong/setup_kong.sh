#!/bin/bash

# Kong API Gateway Setup Script
# This script configures Kong with rate limiting and request size limiting

echo "🚀 Setting up Kong API Gateway..."

# Wait for Kong to be ready
echo "⏳ Waiting for Kong to be ready..."
sleep 10

# Create a service
echo "📦 Creating service..."
curl -i -X POST http://localhost:8001/services/ \
  --data "name=backend-service" \
  --data "url=http://backend-service:80"

# Create a route
echo "🛣️  Creating route..."
curl -i -X POST http://localhost:8001/services/backend-service/routes \
  --data "hosts[]=localhost" \
  --data "paths[]=/api"

# Enable Rate Limiting Plugin (10 requests per minute)
echo "⏱️  Enabling Rate Limiting (10 requests/minute)..."
curl -i -X POST http://localhost:8001/services/backend-service/plugins \
  --data "name=rate-limiting" \
  --data "config.minute=10" \
  --data "config.hour=100" \
  --data "config.policy=local"

# Enable Request Size Limiting Plugin (1MB)
echo "📏 Enabling Request Size Limiting (1MB)..."
curl -i -X POST http://localhost:8001/services/backend-service/plugins \
  --data "name=request-size-limiting" \
  --data "config.allowed_payload_size=1"

echo "✅ Kong setup complete!"
echo ""
echo "📋 Summary:"
echo "  - Service: backend-service"
echo "  - Route: http://localhost:8000/api"
echo "  - Rate Limit: 10 requests/minute"
echo "  - Request Size Limit: 1MB"
echo ""
echo "🧪 Test the setup:"
echo "  curl http://localhost:8000/api"

