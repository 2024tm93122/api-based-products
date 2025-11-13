import requests
import time

API_URL = "http://localhost:8000/api/plagiarism/check"

# Test rate limiting
print("Testing Rate Limiting...")
print("=" * 50)

for i in range(15):
    try:
        response = requests.get(API_URL)
        print(f"Request {i+1:2d}: Status {response.status_code}", end="")
        
        if response.status_code == 200:
            print(" ✓")
        elif response.status_code == 429:
            print(" ✗")
            print(f"  ⚠️  Rate limit exceeded!")
            print(f"  Headers:")
            for header, value in response.headers.items():
                if 'ratelimit' in header.lower():
                    print(f"    {header}: {value}")
            break
        else:
            print(f" (Unexpected: {response.status_code})")
        
        time.sleep(0.5)
    except Exception as e:
        print(f"  Error: {e}")

print("=" * 50)
print("Rate limiting test completed!")