#!/bin/bash

# Kong API Gateway Setup Script
# This script configures Kong with rate limiting and request size limiting

echo "Setting up Kong API Gateway..."

# Wait for Kong to be ready
echo "Waiting for Kong to be ready..."
sleep 10

# Create a service for the backend
echo "Creating service..."
curl -i -X POST http://localhost:8001/services/ \
  --data "name=backend-service" \
  --data "url=http://backend-service:5000"

# Create a route for the service
echo "Creating route..."
curl -i -X POST http://localhost:8001/services/backend-service/routes \
  --data "hosts[]=localhost" \
  --data "paths[]=/api"

# Enable Rate Limiting Plugin (5 requests per minute per consumer)
echo "Enabling Rate Limiting plugin..."
curl -i -X POST http://localhost:8001/services/backend-service/plugins \
  --data "name=rate-limiting" \
  --data "config.minute=5" \
  --data "config.hour=100" \
  --data "config.policy=local"

# Enable Request Size Limiting Plugin (1MB limit)
echo "Enabling Request Size Limiting plugin..."
curl -i -X POST http://localhost:8001/services/backend-service/plugins \
  --data "name=request-size-limiting" \
  --data "config.allowed_payload_size=1"

# Enable Request Termination for testing (optional - to show error handling)
echo "Kong setup completed!"
echo ""
echo "Kong Admin API: http://localhost:8001"
echo "Kong Proxy: http://localhost:8000"
echo ""
echo "Test endpoints:"
echo "  GET http://localhost:8000/api/"
echo "  GET http://localhost:8000/api/data"
echo "  POST http://localhost:8000/api/data"

