"""
Comparison Demo: Token Bucket vs Leaky Bucket Rate Limiting Algorithms

This script demonstrates the differences between Token Bucket and Leaky Bucket algorithms.
"""
import time
from token_bucket import TokenBucketRateLimiter
from leaky_bucket import LeakyBucketRateLimiter


def compare_algorithms():
    """Compare Token Bucket and Leaky Bucket algorithms."""
    print("=" * 70)
    print("Token Bucket vs Leaky Bucket - Comparison Demo")
    print("=" * 70)
    print()
    
    # Create both limiters with same rate: 5 requests/second
    token_limiter = TokenBucketRateLimiter(requests_per_second=5.0, burst_size=10)
    leaky_limiter = LeakyBucketRateLimiter(requests_per_second=5.0, bucket_size=10)
    
    print("Configuration:")
    print("  - Token Bucket: 5 req/s, burst size 10")
    print("  - Leaky Bucket: 5 req/s, bucket size 10")
    print()
    
    # Test 1: Burst of requests
    print("Test 1: Burst of 15 Requests (no delay)")
    print("-" * 70)
    print(f"{'Request':<10} {'Token Bucket':<20} {'Leaky Bucket':<20}")
    print("-" * 70)
    
    token_allowed = 0
    token_denied = 0
    leaky_allowed = 0
    leaky_denied = 0
    
    for i in range(15):
        token_result = "✅ Allowed" if token_limiter.allow_request() else "❌ Denied"
        leaky_result = "✅ Allowed" if leaky_limiter.allow_request() else "❌ Denied"
        
        if "Allowed" in token_result:
            token_allowed += 1
        else:
            token_denied += 1
        
        if "Allowed" in leaky_result:
            leaky_allowed += 1
        else:
            leaky_denied += 1
        
        print(f"{i+1:<10} {token_result:<20} {leaky_result:<20}")
    
    print("-" * 70)
    print(f"Token Bucket: {token_allowed} allowed, {token_denied} denied")
    print(f"Leaky Bucket: {leaky_allowed} allowed, {leaky_denied} denied")
    print()
    
    # Test 2: Steady rate
    print("Test 2: Steady Rate (10 requests with 0.2s delay = 5 req/s)")
    print("-" * 70)
    print(f"{'Request':<10} {'Token Bucket':<20} {'Leaky Bucket':<20}")
    print("-" * 70)
    
    token_allowed = 0
    leaky_allowed = 0
    
    for i in range(10):
        token_result = "✅ Allowed" if token_limiter.allow_request() else "❌ Denied"
        leaky_result = "✅ Allowed" if leaky_limiter.allow_request() else "❌ Denied"
        
        if "Allowed" in token_result:
            token_allowed += 1
        if "Allowed" in leaky_result:
            leaky_allowed += 1
        
        print(f"{i+1:<10} {token_result:<20} {leaky_result:<20}")
        time.sleep(0.2)
    
    print("-" * 70)
    print(f"Token Bucket: {token_allowed} allowed")
    print(f"Leaky Bucket: {leaky_allowed} allowed")
    print()
    
    # Test 3: Status comparison
    print("Test 3: Status Comparison")
    print("-" * 70)
    token_status = token_limiter.get_status()
    leaky_status = leaky_limiter.get_status()
    
    print("Token Bucket Status:")
    print(f"  - Available tokens: {token_status['available_tokens']:.2f}")
    print(f"  - Capacity: {token_status['capacity']}")
    print(f"  - Refill rate: {token_status['refill_rate']} tokens/second")
    print()
    
    print("Leaky Bucket Status:")
    print(f"  - Queue size: {leaky_status['queue_size']}/{leaky_status['capacity']}")
    print(f"  - Available space: {leaky_status['available_space']}")
    print(f"  - Leak rate: {leaky_status['leak_rate']} requests/second")
    print()
    
    # Key differences
    print("=" * 70)
    print("Key Differences:")
    print("=" * 70)
    print("""
1. Token Bucket:
   - Allows bursts up to capacity
   - Tokens accumulate when not used
   - Better for handling traffic spikes
   - More flexible for variable traffic patterns

2. Leaky Bucket:
   - Processes requests at constant rate
   - No accumulation of capacity
   - Smoother output rate
   - Better for maintaining constant processing rate
    """)
    
    print("✅ Comparison complete!")


if __name__ == "__main__":
    compare_algorithms()

