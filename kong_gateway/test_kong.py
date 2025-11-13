"""
Test script for Kong API Gateway rate limiting and request size limiting
"""
import requests
import time
import json

KONG_PROXY = "http://localhost:8000"
KONG_ADMIN = "http://localhost:8001"

def test_rate_limiting():
    """Test rate limiting (5 requests per minute)"""
    print("\n" + "="*50)
    print("Testing Rate Limiting (5 requests/minute)")
    print("="*50)
    
    endpoint = f"{KONG_PROXY}/api/data"
    
    for i in range(7):
        try:
            response = requests.get(endpoint)
            print(f"Request {i+1}: Status {response.status_code}")
            
            if response.status_code == 429:
                print("  ⚠️  Rate limit exceeded!")
                print(f"  Response: {response.text}")
            else:
                print(f"  ✅ Success: {response.json()}")
        
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        time.sleep(1)
    
    print("\nWaiting 60 seconds for rate limit reset...")
    print("(You can test again after the reset)")

def test_request_size_limiting():
    """Test request size limiting (1MB limit)"""
    print("\n" + "="*50)
    print("Testing Request Size Limiting (1MB limit)")
    print("="*50)
    
    endpoint = f"{KONG_PROXY}/api/data"
    
    # Test 1: Small payload (should succeed)
    small_payload = {"data": "x" * 100}  # ~100 bytes
    print("\n1. Testing small payload (~100 bytes)...")
    try:
        response = requests.post(endpoint, json=small_payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Small payload accepted")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Large payload (should fail)
    large_payload = {"data": "x" * 2 * 1024 * 1024}  # 2MB
    print("\n2. Testing large payload (2MB)...")
    try:
        response = requests.post(endpoint, json=large_payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 413:
            print("   ✅ Request size limit enforced (413 Payload Too Large)")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def check_kong_status():
    """Check if Kong is running"""
    try:
        response = requests.get(f"{KONG_ADMIN}/")
        if response.status_code == 200:
            print("✅ Kong is running")
            return True
    except:
        pass
    print("❌ Kong is not running. Please start it first.")
    return False

def get_kong_config():
    """Get current Kong configuration"""
    print("\n" + "="*50)
    print("Kong Configuration")
    print("="*50)
    
    try:
        # Get services
        services = requests.get(f"{KONG_ADMIN}/services").json()
        print(f"\nServices: {len(services.get('data', []))}")
        for service in services.get('data', []):
            print(f"  - {service['name']}: {service['url']}")
        
        # Get plugins
        plugins = requests.get(f"{KONG_ADMIN}/plugins").json()
        print(f"\nPlugins: {len(plugins.get('data', []))}")
        for plugin in plugins.get('data', []):
            print(f"  - {plugin['name']} (enabled: {plugin['enabled']})")
            if 'config' in plugin:
                print(f"    Config: {json.dumps(plugin['config'], indent=4)}")
    
    except Exception as e:
        print(f"Error getting config: {e}")

if __name__ == "__main__":
    print("Kong API Gateway Test Script")
    print("="*50)
    
    if not check_kong_status():
        exit(1)
    
    get_kong_config()
    
    # Run tests
    test_rate_limiting()
    test_request_size_limiting()
    
    print("\n" + "="*50)
    print("Tests completed!")
    print("="*50)

