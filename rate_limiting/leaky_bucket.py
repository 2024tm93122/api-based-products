"""
Leaky Bucket Rate Limiting Algorithm Implementation

The Leaky Bucket algorithm maintains a bucket that leaks at a constant rate.
Requests are added to the bucket. If the bucket is full, requests are rejected.
The bucket leaks (processes requests) at a constant rate.
"""
import time
import threading
from typing import Optional
from collections import deque


class LeakyBucket:
    """
    Leaky Bucket rate limiting implementation.
    
    Attributes:
        capacity: Maximum number of requests the bucket can hold
        leak_rate: Number of requests processed per second
        bucket: Queue of requests in the bucket
        last_leak: Timestamp of the last leak operation
        lock: Thread lock for thread-safe operations
    """
    
    def __init__(self, capacity: int, leak_rate: float):
        """
        Initialize Leaky Bucket.
        
        Args:
            capacity: Maximum number of requests (bucket size)
            leak_rate: Requests processed per second (leak rate)
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if leak_rate <= 0:
            raise ValueError("Leak rate must be positive")
        
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.bucket = deque()  # Queue to hold requests
        self.last_leak = time.time()
        self.lock = threading.Lock()
    
    def _leak_requests(self):
        """Process (leak) requests from the bucket based on elapsed time."""
        current_time = time.time()
        elapsed = current_time - self.last_leak
        
        # Calculate how many requests can be processed
        requests_to_process = int(elapsed * self.leak_rate)
        
        if requests_to_process > 0:
            # Remove processed requests from the front of the queue
            for _ in range(min(requests_to_process, len(self.bucket))):
                self.bucket.popleft()
            
            self.last_leak = current_time
    
    def add_request(self) -> bool:
        """
        Try to add a request to the bucket.
        
        Returns:
            True if request was added, False if bucket is full
        """
        with self.lock:
            self._leak_requests()
            
            if len(self.bucket) < self.capacity:
                self.bucket.append(time.time())  # Store request timestamp
                return True
            else:
                return False
    
    def get_queue_size(self) -> int:
        """
        Get the current number of requests in the bucket.
        
        Returns:
            Number of requests in the bucket
        """
        with self.lock:
            self._leak_requests()
            return len(self.bucket)
    
    def get_wait_time(self) -> float:
        """
        Calculate the estimated wait time for the next request.
        
        Returns:
            Estimated wait time in seconds
        """
        with self.lock:
            self._leak_requests()
            if len(self.bucket) == 0:
                return 0.0
            # Time to process all requests in queue
            return len(self.bucket) / self.leak_rate
    
    def reset(self):
        """Reset the bucket (clear all requests)."""
        with self.lock:
            self.bucket.clear()
            self.last_leak = time.time()


class LeakyBucketRateLimiter:
    """
    Rate limiter using Leaky Bucket algorithm.
    Provides a simple interface for rate limiting requests.
    """
    
    def __init__(self, capacity: int, leak_rate: float):
        """
        Initialize rate limiter.
        
        Args:
            capacity: Maximum number of requests (bucket size)
            leak_rate: Requests processed per second
        """
        self.bucket = LeakyBucket(capacity, leak_rate)
    
    def allow_request(self) -> tuple[bool, Optional[float]]:
        """
        Check if a request should be allowed.
        
        Returns:
            Tuple of (allowed: bool, wait_time: Optional[float])
            wait_time is None if allowed, otherwise seconds to wait
        """
        if self.bucket.add_request():
            return True, None
        else:
            wait_time = self.bucket.get_wait_time()
            return False, wait_time


# Example usage and testing
if __name__ == "__main__":
    print("=" * 60)
    print("Leaky Bucket Rate Limiting Algorithm - Demo")
    print("=" * 60)
    
    # Create a rate limiter: 5 requests capacity, 2 requests per second leak rate
    limiter = LeakyBucketRateLimiter(capacity=5, leak_rate=2.0)
    
    print(f"\nConfiguration:")
    print(f"  Capacity: 5 requests")
    print(f"  Leak Rate: 2 requests/second")
    print(f"\nTesting rate limiting...")
    print("-" * 60)
    
    # Test 1: Fill the bucket quickly
    print("\n1. Adding requests to fill the bucket:")
    for i in range(7):
        allowed, wait_time = limiter.allow_request()
        queue_size = limiter.bucket.get_queue_size()
        if allowed:
            print(f"   Request {i+1}: ✅ ALLOWED (queue size: {queue_size})")
        else:
            print(f"   Request {i+1}: ❌ REJECTED (queue full, wait {wait_time:.2f}s)")
    
    # Test 2: Wait for bucket to leak
    print("\n2. Waiting for bucket to leak (process requests)...")
    time.sleep(2)
    queue_size = limiter.bucket.get_queue_size()
    print(f"   Queue size after 2 seconds: {queue_size}")
    
    # Test 3: Try adding more requests after leak
    print("\n3. Trying to add requests after leak:")
    for i in range(3):
        allowed, wait_time = limiter.allow_request()
        queue_size = limiter.bucket.get_queue_size()
        if allowed:
            print(f"   Request {i+1}: ✅ ALLOWED (queue size: {queue_size})")
        else:
            print(f"   Request {i+1}: ❌ REJECTED (queue full, wait {wait_time:.2f}s)")
    
    # Test 4: Reset bucket
    print("\n4. Resetting bucket:")
    limiter.bucket.reset()
    print(f"   Queue size after reset: {limiter.bucket.get_queue_size()}")
    
    # Test 5: Continuous flow simulation
    print("\n5. Simulating continuous request flow:")
    for i in range(10):
        allowed, wait_time = limiter.allow_request()
        queue_size = limiter.bucket.get_queue_size()
        if allowed:
            print(f"   Request {i+1}: ✅ ALLOWED (queue: {queue_size})")
        else:
            print(f"   Request {i+1}: ❌ REJECTED (wait {wait_time:.2f}s)")
        time.sleep(0.3)  # Small delay between requests
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)

