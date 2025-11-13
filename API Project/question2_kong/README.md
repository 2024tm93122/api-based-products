# Question 2: Kong API Gateway - Rate Limiting & Request Size Limiting

This directory contains the setup for Kong API Gateway with rate limiting and request size limiting configurations.

## 📋 Prerequisites

- Docker and Docker Compose installed
- Ports 8000, 8001, 8080 available

## 🚀 Setup Instructions

### Step 1: Start Kong and Services

```bash
docker-compose up -d
```

Wait for all services to be healthy (about 30 seconds).

### Step 2: Configure Kong

**For Linux/Mac:**
```bash
chmod +x setup_kong.sh
./setup_kong.sh
```

**For Windows PowerShell:**
```powershell
.\setup_kong.ps1
```

**Manual Setup (Alternative):**

If the scripts don't work, you can configure Kong manually:

1. **Create Service:**
```bash
curl -i -X POST http://localhost:8001/services/ \
  --data "name=backend-service" \
  --data "url=http://backend-service:80"
```

2. **Create Route:**
```bash
curl -i -X POST http://localhost:8001/services/backend-service/routes \
  --data "hosts[]=localhost" \
  --data "paths[]=/api"
```

3. **Enable Rate Limiting (10 requests/minute):**
```bash
curl -i -X POST http://localhost:8001/services/backend-service/plugins \
  --data "name=rate-limiting" \
  --data "config.minute=10" \
  --data "config.hour=100" \
  --data "config.policy=local"
```

4. **Enable Request Size Limiting (1MB):**
```bash
curl -i -X POST http://localhost:8001/services/backend-service/plugins \
  --data "name=request-size-limiting" \
  --data "config.allowed_payload_size=1"
```

## 🧪 Testing

### Test Rate Limiting

```bash
# Make multiple requests quickly
for i in {1..15}; do
  curl http://localhost:8000/api
  echo ""
done
```

After 10 requests, you should see `429 Too Many Requests` responses.

### Test Request Size Limiting

```bash
# Small payload (should succeed)
curl -X POST http://localhost:8000/api \
  -H "Content-Type: application/json" \
  -d '{"data": "small test"}'

# Large payload (should fail with 413)
curl -X POST http://localhost:8000/api \
  -H "Content-Type: application/json" \
  -d '{"data": "'$(python -c "print('x' * 2000000)")'"}'
```

### Using Python Test Script

```bash
pip install requests
python test_rate_limit.py
```

## 📊 Configuration Details

### Rate Limiting
- **Limit:** 10 requests per minute
- **Hourly Limit:** 100 requests per hour
- **Policy:** Local (in-memory)

### Request Size Limiting
- **Maximum Size:** 1MB (1,048,576 bytes)
- **Response:** 413 Payload Too Large

## 🔍 Verify Configuration

Check Kong Admin API:

```bash
# List services
curl http://localhost:8001/services/

# List routes
curl http://localhost:8001/routes/

# List plugins
curl http://localhost:8001/plugins/
```

## 🛑 Stop Services

```bash
docker-compose down
```

To remove volumes:
```bash
docker-compose down -v
```

## 📸 Screenshots for Assignment

1. **Kong Admin API** - Show services, routes, and plugins configured
2. **Rate Limiting Test** - Show 429 responses after exceeding limit
3. **Request Size Limiting Test** - Show 413 response for large payloads
4. **Kong Dashboard** (if using Konga) - Visual configuration

## 📝 Notes

- Rate limiting uses local policy (in-memory), suitable for single Kong instance
- For distributed systems, use Redis policy
- Request size is in MB (1 = 1MB)
- All configurations are stored in PostgreSQL database

