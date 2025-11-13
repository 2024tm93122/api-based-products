"""
Comparison Demo: Token Bucket vs Leaky Bucket

This script demonstrates the differences between Token Bucket and Leaky Bucket
rate limiting algorithms with side-by-side comparisons.
"""
import time
from token_bucket import TokenBucketRateLimiter
from leaky_bucket import LeakyBucketRateLimiter


def simulate_requests(limiter, name, num_requests=10, delay=0.1):
    """
    Simulate a series of requests through a rate limiter.
    
    Args:
        limiter: Rate limiter instance
        name: Name of the limiter
        num_requests: Number of requests to simulate
        delay: Delay between requests in seconds
    """
    print(f"\n{'='*60}")
    print(f"{name} - Simulating {num_requests} requests")
    print(f"{'='*60}")
    
    allowed_count = 0
    rejected_count = 0
    
    for i in range(num_requests):
        allowed, wait_time = limiter.allow_request()
        
        if allowed:
            allowed_count += 1
            status = "✅ ALLOWED"
        else:
            rejected_count += 1
            status = f"❌ REJECTED (wait {wait_time:.2f}s)"
        
        if isinstance(limiter, TokenBucketRateLimiter):
            tokens = limiter.bucket.get_available_tokens()
            print(f"Request {i+1:2d}: {status} | Tokens: {tokens:.2f}")
        else:
            queue_size = limiter.bucket.get_queue_size()
            print(f"Request {i+1:2d}: {status} | Queue: {queue_size}")
        
        time.sleep(delay)
    
    print(f"\nSummary: {allowed_count} allowed, {rejected_count} rejected")


def burst_test():
    """Test how each algorithm handles burst traffic."""
    print("\n" + "="*60)
    print("BURST TRAFFIC TEST")
    print("="*60)
    print("Configuration: Capacity=5, Rate=2/sec")
    print("Test: 10 requests sent quickly (burst)")
    
    token_limiter = TokenBucketRateLimiter(capacity=5, refill_rate=2.0)
    leaky_limiter = LeakyBucketRateLimiter(capacity=5, leak_rate=2.0)
    
    print("\n" + "-"*60)
    print("TOKEN BUCKET (Burst Test)")
    print("-"*60)
    
    # Token Bucket: Can handle burst if tokens are available
    for i in range(10):
        allowed, wait_time = token_limiter.allow_request()
        tokens = token_limiter.bucket.get_available_tokens()
        status = "✅" if allowed else f"❌ (wait {wait_time:.2f}s)"
        print(f"Request {i+1:2d}: {status} | Tokens: {tokens:.2f}")
    
    print("\n" + "-"*60)
    print("LEAKY BUCKET (Burst Test)")
    print("-"*60)
    
    # Leaky Bucket: Processes at constant rate
    for i in range(10):
        allowed, wait_time = leaky_limiter.allow_request()
        queue_size = leaky_limiter.bucket.get_queue_size()
        status = "✅" if allowed else f"❌ (wait {wait_time:.2f}s)"
        print(f"Request {i+1:2d}: {status} | Queue: {queue_size}")


def steady_state_test():
    """Test how each algorithm handles steady-state traffic."""
    print("\n" + "="*60)
    print("STEADY-STATE TRAFFIC TEST")
    print("="*60)
    print("Configuration: Capacity=5, Rate=2/sec")
    print("Test: Requests sent at 1 request per 0.4 seconds (2.5 req/sec)")
    
    token_limiter = TokenBucketRateLimiter(capacity=5, refill_rate=2.0)
    leaky_limiter = LeakyBucketRateLimiter(capacity=5, leak_rate=2.0)
    
    print("\n" + "-"*60)
    print("TOKEN BUCKET (Steady State)")
    print("-"*60)
    
    for i in range(10):
        allowed, wait_time = token_limiter.allow_request()
        tokens = token_limiter.bucket.get_available_tokens()
        status = "✅" if allowed else f"❌ (wait {wait_time:.2f}s)"
        print(f"Request {i+1:2d}: {status} | Tokens: {tokens:.2f}")
        time.sleep(0.4)
    
    print("\n" + "-"*60)
    print("LEAKY BUCKET (Steady State)")
    print("-"*60)
    
    for i in range(10):
        allowed, wait_time = leaky_limiter.allow_request()
        queue_size = leaky_limiter.bucket.get_queue_size()
        status = "✅" if allowed else f"❌ (wait {wait_time:.2f}s)"
        print(f"Request {i+1:2d}: {status} | Queue: {queue_size}")
        time.sleep(0.4)


def main():
    """Run comparison demos."""
    print("="*60)
    print("TOKEN BUCKET vs LEAKY BUCKET - COMPARISON")
    print("="*60)
    
    print("\nKey Differences:")
    print("1. Token Bucket: Allows bursts if tokens available")
    print("2. Leaky Bucket: Smooths out traffic, constant output rate")
    print("3. Token Bucket: Better for allowing occasional bursts")
    print("4. Leaky Bucket: Better for smoothing traffic patterns")
    
    # Run tests
    burst_test()
    time.sleep(2)
    steady_state_test()
    
    print("\n" + "="*60)
    print("COMPARISON COMPLETED")
    print("="*60)


if __name__ == "__main__":
    main()

