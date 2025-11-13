"""
Token Bucket Rate Limiting Algorithm Implementation

The Token Bucket algorithm maintains a bucket with a maximum capacity of tokens.
Tokens are added to the bucket at a constant rate. When a request arrives,
it consumes a token. If no tokens are available, the request is rejected.
"""
import time
import threading
from typing import Optional


class TokenBucket:
    """
    Token Bucket rate limiting implementation.
    
    Attributes:
        capacity: Maximum number of tokens the bucket can hold
        refill_rate: Number of tokens added per second
        tokens: Current number of tokens in the bucket
        last_refill: Timestamp of the last token refill
        lock: Thread lock for thread-safe operations
    """
    
    def __init__(self, capacity: int, refill_rate: float):
        """
        Initialize Token Bucket.
        
        Args:
            capacity: Maximum number of tokens (bucket size)
            refill_rate: Tokens added per second
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity  # Start with full bucket
        self.last_refill = time.time()
        self.lock = threading.Lock()
    
    def _refill_tokens(self):
        """Refill tokens based on elapsed time since last refill."""
        current_time = time.time()
        elapsed = current_time - self.last_refill
        
        # Calculate tokens to add
        tokens_to_add = elapsed * self.refill_rate
        
        if tokens_to_add > 0:
            self.tokens = min(self.capacity, self.tokens + tokens_to_add)
            self.last_refill = current_time
    
    def consume(self, tokens: int = 1) -> bool:
        """
        Try to consume tokens from the bucket.
        
        Args:
            tokens: Number of tokens to consume (default: 1)
        
        Returns:
            True if tokens were consumed, False if insufficient tokens
        """
        with self.lock:
            self._refill_tokens()
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            else:
                return False
    
    def get_available_tokens(self) -> float:
        """
        Get the current number of available tokens.
        
        Returns:
            Number of available tokens
        """
        with self.lock:
            self._refill_tokens()
            return self.tokens
    
    def reset(self):
        """Reset the bucket to full capacity."""
        with self.lock:
            self.tokens = self.capacity
            self.last_refill = time.time()


class TokenBucketRateLimiter:
    """
    Rate limiter using Token Bucket algorithm.
    Provides a simple interface for rate limiting requests.
    """
    
    def __init__(self, capacity: int, refill_rate: float):
        """
        Initialize rate limiter.
        
        Args:
            capacity: Maximum number of requests (tokens)
            refill_rate: Requests allowed per second
        """
        self.bucket = TokenBucket(capacity, refill_rate)
    
    def allow_request(self) -> tuple[bool, Optional[float]]:
        """
        Check if a request should be allowed.
        
        Returns:
            Tuple of (allowed: bool, wait_time: Optional[float])
            wait_time is None if allowed, otherwise seconds to wait
        """
        if self.bucket.consume():
            return True, None
        else:
            # Calculate wait time
            available = self.bucket.get_available_tokens()
            wait_time = (1 - available) / self.bucket.refill_rate
            return False, max(0, wait_time)


# Example usage and testing
if __name__ == "__main__":
    print("=" * 60)
    print("Token Bucket Rate Limiting Algorithm - Demo")
    print("=" * 60)
    
    # Create a rate limiter: 5 requests capacity, 2 requests per second refill
    limiter = TokenBucketRateLimiter(capacity=5, refill_rate=2.0)
    
    print(f"\nConfiguration:")
    print(f"  Capacity: 5 tokens")
    print(f"  Refill Rate: 2 tokens/second")
    print(f"\nTesting rate limiting...")
    print("-" * 60)
    
    # Test 1: Consume all tokens quickly
    print("\n1. Consuming all tokens quickly:")
    for i in range(7):
        allowed, wait_time = limiter.allow_request()
        if allowed:
            print(f"   Request {i+1}: ✅ ALLOWED (tokens: {limiter.bucket.get_available_tokens():.2f})")
        else:
            print(f"   Request {i+1}: ❌ REJECTED (wait {wait_time:.2f}s)")
    
    # Test 2: Wait and refill
    print("\n2. Waiting for token refill...")
    time.sleep(2)
    print(f"   Available tokens after 2 seconds: {limiter.bucket.get_available_tokens():.2f}")
    
    # Test 3: Try again after refill
    print("\n3. Trying requests after refill:")
    for i in range(3):
        allowed, wait_time = limiter.allow_request()
        if allowed:
            print(f"   Request {i+1}: ✅ ALLOWED (tokens: {limiter.bucket.get_available_tokens():.2f})")
        else:
            print(f"   Request {i+1}: ❌ REJECTED (wait {wait_time:.2f}s)")
    
    # Test 4: Reset bucket
    print("\n4. Resetting bucket:")
    limiter.bucket.reset()
    print(f"   Available tokens after reset: {limiter.bucket.get_available_tokens():.2f}")
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)

