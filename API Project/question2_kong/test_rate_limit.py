"""
Test script to demonstrate rate limiting and request size limiting in Kong API Gateway.
"""
import requests
import time
import json


API_URL = "http://localhost:8000/api"


def test_rate_limiting():
    """Test rate limiting by making multiple requests quickly."""
    print("🧪 Testing Rate Limiting (10 requests/minute)...")
    print("-" * 50)
    
    success_count = 0
    rate_limited_count = 0
    
    for i in range(15):
        try:
            response = requests.get(API_URL, timeout=5)
            if response.status_code == 200:
                success_count += 1
                print(f"✅ Request {i+1}: Success (Status: {response.status_code})")
            elif response.status_code == 429:
                rate_limited_count += 1
                print(f"⛔ Request {i+1}: Rate Limited (Status: {response.status_code})")
                # Check for rate limit headers
                if 'X-RateLimit-Remaining-Minute' in response.headers:
                    print(f"   Remaining requests: {response.headers['X-RateLimit-Remaining-Minute']}")
        except Exception as e:
            print(f"❌ Request {i+1}: Error - {str(e)}")
        
        time.sleep(0.5)  # Small delay between requests
    
    print("-" * 50)
    print(f"📊 Results: {success_count} successful, {rate_limited_count} rate limited")
    print()


def test_request_size_limiting():
    """Test request size limiting by sending a large payload."""
    print("🧪 Testing Request Size Limiting (1MB limit)...")
    print("-" * 50)
    
    # Test with small payload (should succeed)
    small_payload = {"data": "small test data"}
    print("📤 Sending small payload (< 1MB)...")
    try:
        response = requests.post(API_URL, json=small_payload, timeout=5)
        print(f"✅ Small payload: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Small payload error: {str(e)}")
    
    # Test with large payload (should fail)
    large_payload = {"data": "x" * (2 * 1024 * 1024)}  # 2MB payload
    print("📤 Sending large payload (> 1MB)...")
    try:
        response = requests.post(API_URL, json=large_payload, timeout=5)
        if response.status_code == 413:
            print(f"⛔ Large payload: Request too large (Status: {response.status_code})")
        else:
            print(f"⚠️  Large payload: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Large payload error: {str(e)}")
    
    print("-" * 50)
    print()


if __name__ == "__main__":
    print("=" * 50)
    print("Kong API Gateway - Rate Limiting & Size Limiting Tests")
    print("=" * 50)
    print()
    
    # Check if Kong is running
    try:
        response = requests.get("http://localhost:8001/", timeout=2)
        print("✅ Kong Admin API is accessible")
    except:
        print("❌ Kong Admin API is not accessible. Please start Kong first.")
        print("   Run: docker-compose up -d")
        exit(1)
    
    print()
    test_rate_limiting()
    test_request_size_limiting()
    
    print("✅ Testing complete!")

