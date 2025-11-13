"""
Token Bucket Rate Limiting Algorithm

Concept:
- A bucket holds tokens with a maximum capacity
- Tokens are added at a fixed rate
- Each request consumes one token
- If no tokens available, request is rejected
- Allows burst traffic up to bucket capacity

Use Case: API rate limiting, network traffic shaping
"""

import time
import threading
from typing import Optional


class TokenBucket:
    """
    Token Bucket implementation for rate limiting.
    
    Args:
        capacity: Maximum number of tokens in bucket
        refill_rate: Number of tokens added per second
    """
    
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill_time = time.time()
        self.lock = threading.Lock()
    
    def _refill(self):
        """Refill tokens based on elapsed time"""
        now = time.time()
        elapsed = now - self.last_refill_time
        
        # Calculate tokens to add
        tokens_to_add = elapsed * self.refill_rate
        
        # Add tokens but don't exceed capacity
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill_time = now
    
    def consume(self, tokens: int = 1) -> bool:
        """
        Try to consume tokens from bucket.
        
        Args:
            tokens: Number of tokens to consume
            
        Returns:
            True if tokens consumed successfully, False otherwise
        """
        with self.lock:
            self._refill()
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def get_available_tokens(self) -> float:
        """Get current number of available tokens"""
        with self.lock:
            self._refill()
            return self.tokens
    
    def wait_time_for_tokens(self, tokens: int = 1) -> float:
        """
        Calculate wait time until requested tokens are available.
        
        Args:
            tokens: Number of tokens needed
            
        Returns:
            Time to wait in seconds
        """
        with self.lock:
            self._refill()
            
            if self.tokens >= tokens:
                return 0.0
            
            tokens_needed = tokens - self.tokens
            return tokens_needed / self.refill_rate


class TokenBucketRateLimiter:
    """
    Rate limiter using Token Bucket algorithm.
    Manages multiple buckets for different clients.
    """
    
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.buckets = {}
        self.lock = threading.Lock()
    
    def allow_request(self, client_id: str, tokens: int = 1) -> tuple[bool, Optional[float]]:
        """
        Check if request is allowed for client.
        
        Args:
            client_id: Unique identifier for client
            tokens: Number of tokens to consume
            
        Returns:
            Tuple of (allowed: bool, retry_after: Optional[float])
        """
        with self.lock:
            if client_id not in self.buckets:
                self.buckets[client_id] = TokenBucket(self.capacity, self.refill_rate)
        
        bucket = self.buckets[client_id]
        
        if bucket.consume(tokens):
            return True, None
        else:
            retry_after = bucket.wait_time_for_tokens(tokens)
            return False, retry_after
    
    def get_client_info(self, client_id: str) -> dict:
        """Get information about client's bucket"""
        with self.lock:
            if client_id not in self.buckets:
                return {
                    "client_id": client_id,
                    "tokens_available": self.capacity,
                    "capacity": self.capacity,
                    "refill_rate": self.refill_rate
                }
            
            bucket = self.buckets[client_id]
            return {
                "client_id": client_id,
                "tokens_available": bucket.get_available_tokens(),
                "capacity": self.capacity,
                "refill_rate": self.refill_rate
            }


# ============================================================================
# DEMONSTRATION AND TESTING
# ============================================================================

def demonstrate_token_bucket():
    """Demonstrate Token Bucket algorithm"""
    
    print("=" * 70)
    print("TOKEN BUCKET RATE LIMITING ALGORITHM - DEMONSTRATION")
    print("=" * 70)
    
    # Create rate limiter: 10 tokens capacity, 2 tokens per second
    rate_limiter = TokenBucketRateLimiter(capacity=10, refill_rate=2.0)
    
    print("\nConfiguration:")
    print(f"  - Bucket Capacity: 10 tokens")
    print(f"  - Refill Rate: 2 tokens/second")
    print(f"  - Initial State: Bucket is full (10 tokens)")
    
    # Test 1: Burst requests (should allow up to capacity)
    print("\n" + "=" * 70)
    print("Test 1: BURST REQUESTS (Testing bucket capacity)")
    print("=" * 70)
    
    client_id = "user_123"
    
    for i in range(12):
        allowed, retry_after = rate_limiter.allow_request(client_id)
        info = rate_limiter.get_client_info(client_id)
        
        status = "✅ ALLOWED" if allowed else "❌ REJECTED"
        print(f"Request {i+1:2d}: {status} | Tokens remaining: {info['tokens_available']:.2f}")
        
        if not allowed:
            print(f"           → Retry after: {retry_after:.2f} seconds")
    
    # Test 2: Steady state requests with refill
    print("\n" + "=" * 70)
    print("Test 2: STEADY STATE (Testing refill mechanism)")
    print("=" * 70)
    print("Waiting for tokens to refill...")
    
    time.sleep(3)  # Wait for some tokens to refill
    
    client_id = "user_456"
    
    for i in range(8):
        allowed, retry_after = rate_limiter.allow_request(client_id)
        info = rate_limiter.get_client_info(client_id)
        
        status = "✅ ALLOWED" if allowed else "❌ REJECTED"
        print(f"Request {i+1}: {status} | Tokens: {info['tokens_available']:.2f}")
        
        time.sleep(0.3)  # Small delay between requests
    
    # Test 3: Multiple clients
    print("\n" + "=" * 70)
    print("Test 3: MULTIPLE CLIENTS (Independent buckets)")
    print("=" * 70)
    
    clients = ["client_A", "client_B", "client_C"]
    
    for client in clients:
        print(f"\n{client}:")
        for i in range(5):
            allowed, _ = rate_limiter.allow_request(client)
            info = rate_limiter.get_client_info(client)
            status = "✅" if allowed else "❌"
            print(f"  Request {i+1}: {status} | Tokens: {info['tokens_available']:.2f}")
    
    # Test 4: Token consumption with different weights
    print("\n" + "=" * 70)
    print("Test 4: WEIGHTED REQUESTS (Different token costs)")
    print("=" * 70)
    
    client_id = "user_heavy"
    
    # Reset by using new client
    test_requests = [
        (1, "Light request"),
        (3, "Medium request"),
        (5, "Heavy request"),
        (2, "Light-medium request"),
    ]
    
    for tokens, description in test_requests:
        allowed, retry_after = rate_limiter.allow_request(client_id, tokens)
        info = rate_limiter.get_client_info(client_id)
        
        status = "✅ ALLOWED" if allowed else "❌ REJECTED"
        print(f"{description} ({tokens} tokens): {status}")
        print(f"  → Tokens remaining: {info['tokens_available']:.2f}")
        
        if not allowed and retry_after:
            print(f"  → Retry after: {retry_after:.2f}s")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY: Token Bucket Characteristics")
    print("=" * 70)
    print("""
✓ Allows burst traffic up to bucket capacity
✓ Smooth rate limiting with continuous refill
✓ Each client has independent bucket
✓ Supports weighted requests (variable token costs)
✓ Provides retry-after information
✓ Memory efficient - one bucket per client

Use Cases:
- API rate limiting (requests per second)
- Network traffic shaping
- Resource quota management
- Microservices communication throttling
    """)


def simulate_api_server():
    """Simulate an API server with token bucket rate limiting"""
    
    print("\n" + "=" * 70)
    print("SIMULATED API SERVER WITH TOKEN BUCKET RATE LIMITING")
    print("=" * 70)
    
    # Create API rate limiter: 5 requests per second per client
    api_limiter = TokenBucketRateLimiter(capacity=20, refill_rate=5.0)
    
    def handle_request(client_id: str, endpoint: str):
        """Simulate handling an API request"""
        allowed, retry_after = api_limiter.allow_request(client_id)
        
        if allowed:
            return {
                "status": 200,
                "message": f"Request to {endpoint} successful",
                "client": client_id
            }
        else:
            return {
                "status": 429,
                "message": "Rate limit exceeded",
                "retry_after": retry_after,
                "client": client_id
            }
    
    # Simulate API traffic
    print("\nSimulating API traffic from multiple clients...\n")
    
    scenarios = [
        ("user_1", "/api/users", 15),
        ("user_2", "/api/products", 10),
        ("user_1", "/api/orders", 5),
    ]
    
    for client, endpoint, num_requests in scenarios:
        print(f"\n{client} making {num_requests} requests to {endpoint}:")
        
        for i in range(num_requests):
            response = handle_request(client, endpoint)
            
            if response["status"] == 200:
                print(f"  ✅ Request {i+1}: {response['message']}")
            else:
                print(f"  ❌ Request {i+1}: {response['message']} (retry after {response['retry_after']:.2f}s)")
            
            time.sleep(0.1)
        
        info = api_limiter.get_client_info(client)
        print(f"  📊 Remaining tokens: {info['tokens_available']:.2f}")


if __name__ == "__main__":
    # Run demonstration
    demonstrate_token_bucket()
    
    # Run API simulation
    simulate_api_server()
    
    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)
