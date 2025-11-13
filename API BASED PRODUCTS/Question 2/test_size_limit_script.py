import requests
import os

API_URL = "http://localhost:8000/api/plagiarism/check"

# Test request size limiting
print("Testing Request Size Limiting...")
print("=" * 50)

# Create a large file (6MB - exceeds 5MB limit)
large_content = "A" * (6 * 1024 * 1024)  # 6MB of 'A's
filename = 'large_file.txt'

with open(filename, 'w') as f:
    f.write(large_content)

file_size = os.path.getsize(filename) / (1024 * 1024)
print(f"Created test file: {filename} ({file_size:.2f} MB)")
print()

# Try to upload large file
try:
    files = {
        'original': open(filename, 'rb'),
        'submission': open(filename, 'rb')
    }
    
    print("Attempting to upload files...")
    response = requests.post(API_URL, files=files)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 413:
        print("✅ Request size limit working!")
        print(f"Response: {response.text}")
    elif response.status_code == 200:
        print("⚠️  Warning: File was accepted (size limit may not be configured)")
    else:
        print(f"Unexpected response: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"Error: {e}")

finally:
    # Clean up
    if os.path.exists(filename):
        os.remove(filename)
        print(f"\nCleaned up: {filename}")

print("=" * 50)
print("Size limiting test completed!")