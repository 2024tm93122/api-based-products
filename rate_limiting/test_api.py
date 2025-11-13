"""
Test script for rate limiting API server.
"""
import requests
import time

BASE_URL = "http://localhost:5001"


def test_token_bucket():
    """Test Token Bucket rate limiting."""
    print("\n" + "="*60)
    print("Testing Token Bucket Rate Limiting")
    print("="*60)
    
    endpoint = f"{BASE_URL}/api/token-bucket"
    
    print("\nSending 15 requests quickly (capacity: 10, rate: 5/sec)...")
    for i in range(15):
        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                data = response.json()
                print(f"Request {i+1:2d}: ✅ ALLOWED (tokens: {data['available_tokens']:.2f})")
            elif response.status_code == 429:
                data = response.json()
                print(f"Request {i+1:2d}: ❌ RATE LIMITED (wait {data['wait_time_seconds']:.2f}s)")
            else:
                print(f"Request {i+1:2d}: ⚠️  Status {response.status_code}")
        except Exception as e:
            print(f"Request {i+1:2d}: ❌ Error: {e}")
        
        time.sleep(0.1)


def test_leaky_bucket():
    """Test Leaky Bucket rate limiting."""
    print("\n" + "="*60)
    print("Testing Leaky Bucket Rate Limiting")
    print("="*60)
    
    endpoint = f"{BASE_URL}/api/leaky-bucket"
    
    print("\nSending 15 requests quickly (capacity: 10, rate: 5/sec)...")
    for i in range(15):
        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                data = response.json()
                print(f"Request {i+1:2d}: ✅ ALLOWED (queue: {data['queue_size']})")
            elif response.status_code == 429:
                data = response.json()
                print(f"Request {i+1:2d}: ❌ RATE LIMITED (wait {data['wait_time_seconds']:.2f}s)")
            else:
                print(f"Request {i+1:2d}: ⚠️  Status {response.status_code}")
        except Exception as e:
            print(f"Request {i+1:2d}: ❌ Error: {e}")
        
        time.sleep(0.1)


def test_stats():
    """Test stats endpoint."""
    print("\n" + "="*60)
    print("Getting Rate Limiter Statistics")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/stats")
        if response.status_code == 200:
            data = response.json()
            print("\nToken Bucket:")
            print(f"  Available Tokens: {data['token_bucket']['available_tokens']:.2f}")
            print(f"  Capacity: {data['token_bucket']['capacity']}")
            print(f"  Refill Rate: {data['token_bucket']['refill_rate']} tokens/sec")
            
            print("\nLeaky Bucket:")
            print(f"  Queue Size: {data['leaky_bucket']['queue_size']}")
            print(f"  Capacity: {data['leaky_bucket']['capacity']}")
            print(f"  Leak Rate: {data['leaky_bucket']['leak_rate']} requests/sec")
        else:
            print(f"Error: Status {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Run all tests."""
    print("="*60)
    print("Rate Limiting API Test Suite")
    print("="*60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ API server is running")
        else:
            print("⚠️  API server may not be ready")
    except:
        print("❌ API server is not running!")
        print("Please start the server first: python api_server.py")
        return
    
    # Reset limiters
    try:
        requests.post(f"{BASE_URL}/api/reset")
        print("✅ Rate limiters reset")
    except:
        pass
    
    # Run tests
    test_token_bucket()
    time.sleep(2)
    
    # Reset and test leaky bucket
    try:
        requests.post(f"{BASE_URL}/api/reset")
    except:
        pass
    
    test_leaky_bucket()
    test_stats()
    
    print("\n" + "="*60)
    print("Tests completed!")
    print("="*60)


if __name__ == "__main__":
    main()

