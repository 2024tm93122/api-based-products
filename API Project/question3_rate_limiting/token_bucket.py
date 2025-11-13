"""
Token Bucket Rate Limiting Algorithm Implementation

The Token Bucket algorithm maintains a bucket with a maximum capacity of tokens.
Tokens are added to the bucket at a constant rate. When a request arrives,
it consumes a token. If no tokens are available, the request is rejected.
"""
import time
import threading
from typing import Optional
from dataclasses import dataclass


@dataclass
class TokenBucketConfig:
    """Configuration for Token Bucket algorithm."""
    capacity: int  # Maximum number of tokens
    refill_rate: float  # Tokens added per second
    initial_tokens: Optional[int] = None  # Initial tokens (defaults to capacity)


class TokenBucket:
    """
    Token Bucket rate limiting implementation.
    
    Attributes:
        capacity: Maximum number of tokens the bucket can hold
        refill_rate: Number of tokens added per second
        tokens: Current number of tokens in the bucket
        last_refill: Timestamp of last token refill
        lock: Thread lock for thread-safe operations
    """
    
    def __init__(self, capacity: int, refill_rate: float, initial_tokens: Optional[int] = None):
        """
        Initialize Token Bucket.
        
        Args:
            capacity: Maximum number of tokens
            refill_rate: Tokens added per second
            initial_tokens: Initial token count (defaults to capacity)
        """
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be greater than 0")
        
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = initial_tokens if initial_tokens is not None else capacity
        self.last_refill = time.time()
        self.lock = threading.Lock()
    
    def _refill_tokens(self):
        """Refill tokens based on elapsed time."""
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
            True if tokens were consumed, False otherwise
        """
        with self.lock:
            self._refill_tokens()
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def get_available_tokens(self) -> float:
        """
        Get the current number of available tokens.
        
        Returns:
            Current token count
        """
        with self.lock:
            self._refill_tokens()
            return self.tokens
    
    def get_wait_time(self, tokens: int = 1) -> float:
        """
        Calculate time to wait before tokens become available.
        
        Args:
            tokens: Number of tokens needed
        
        Returns:
            Seconds to wait (0 if tokens are available)
        """
        with self.lock:
            self._refill_tokens()
            
            if self.tokens >= tokens:
                return 0.0
            
            tokens_needed = tokens - self.tokens
            return tokens_needed / self.refill_rate


class TokenBucketRateLimiter:
    """
    Rate limiter using Token Bucket algorithm.
    Provides a simple interface for rate limiting requests.
    """
    
    def __init__(self, requests_per_second: float, burst_size: Optional[int] = None):
        """
        Initialize rate limiter.
        
        Args:
            requests_per_second: Maximum requests per second
            burst_size: Maximum burst size (defaults to requests_per_second)
        """
        burst = burst_size if burst_size is not None else int(requests_per_second)
        self.bucket = TokenBucket(
            capacity=burst,
            refill_rate=requests_per_second,
            initial_tokens=burst
        )
    
    def allow_request(self) -> bool:
        """
        Check if a request should be allowed.
        
        Returns:
            True if request is allowed, False otherwise
        """
        return self.bucket.consume(1)
    
    def get_status(self) -> dict:
        """
        Get current status of the rate limiter.
        
        Returns:
            Dictionary with status information
        """
        available = self.bucket.get_available_tokens()
        wait_time = self.bucket.get_wait_time(1)
        
        return {
            "available_tokens": available,
            "capacity": self.bucket.capacity,
            "refill_rate": self.bucket.refill_rate,
            "wait_time_seconds": wait_time
        }


# Example usage and testing
if __name__ == "__main__":
    print("=" * 60)
    print("Token Bucket Rate Limiting Algorithm - Demo")
    print("=" * 60)
    print()
    
    # Create a rate limiter: 5 requests per second, burst of 10
    limiter = TokenBucketRateLimiter(requests_per_second=5.0, burst_size=10)
    
    print("Configuration:")
    print(f"  - Requests per second: 5.0")
    print(f"  - Burst size: 10")
    print()
    
    # Test 1: Burst requests
    print("Test 1: Burst Requests (15 requests)")
    print("-" * 60)
    allowed = 0
    denied = 0
    
    for i in range(15):
        if limiter.allow_request():
            allowed += 1
            print(f"Request {i+1}: ✅ Allowed")
        else:
            denied += 1
            print(f"Request {i+1}: ❌ Denied")
    
    print(f"\nResults: {allowed} allowed, {denied} denied")
    print()
    
    # Test 2: Steady rate
    print("Test 2: Steady Rate (10 requests with 0.2s delay)")
    print("-" * 60)
    allowed = 0
    denied = 0
    
    for i in range(10):
        if limiter.allow_request():
            allowed += 1
            print(f"Request {i+1}: ✅ Allowed (Tokens: {limiter.bucket.get_available_tokens():.2f})")
        else:
            denied += 1
            print(f"Request {i+1}: ❌ Denied")
        time.sleep(0.2)  # 0.2s = 5 requests per second
    
    print(f"\nResults: {allowed} allowed, {denied} denied")
    print()
    
    # Test 3: Status check
    print("Test 3: Status Check")
    print("-" * 60)
    status = limiter.get_status()
    print(f"Available tokens: {status['available_tokens']:.2f}")
    print(f"Capacity: {status['capacity']}")
    print(f"Refill rate: {status['refill_rate']} tokens/second")
    print(f"Wait time for next token: {status['wait_time_seconds']:.2f} seconds")
    print()
    
    print("✅ Token Bucket algorithm demonstration complete!")

