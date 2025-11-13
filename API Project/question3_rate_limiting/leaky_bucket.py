"""
Leaky Bucket Rate Limiting Algorithm Implementation

The Leaky Bucket algorithm maintains a bucket with a maximum capacity.
Requests are added to the bucket. The bucket leaks at a constant rate,
processing requests. If the bucket is full, new requests are rejected.
"""
import time
import threading
from typing import Optional
from dataclasses import dataclass
from collections import deque


@dataclass
class LeakyBucketConfig:
    """Configuration for Leaky Bucket algorithm."""
    capacity: int  # Maximum number of requests in bucket
    leak_rate: float  # Requests processed per second
    initial_size: int = 0  # Initial number of requests in bucket


class LeakyBucket:
    """
    Leaky Bucket rate limiting implementation.
    
    Attributes:
        capacity: Maximum number of requests the bucket can hold
        leak_rate: Number of requests processed per second
        queue: Queue of requests waiting to be processed
        last_leak: Timestamp of last leak operation
        lock: Thread lock for thread-safe operations
    """
    
    def __init__(self, capacity: int, leak_rate: float, initial_size: int = 0):
        """
        Initialize Leaky Bucket.
        
        Args:
            capacity: Maximum number of requests
            leak_rate: Requests processed per second
            initial_size: Initial number of requests (default: 0)
        """
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")
        if leak_rate <= 0:
            raise ValueError("Leak rate must be greater than 0")
        
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.queue = deque(maxlen=capacity)
        self.last_leak = time.time()
        self.lock = threading.Lock()
        
        # Initialize with some requests if specified
        for _ in range(min(initial_size, capacity)):
            self.queue.append(time.time())
    
    def _leak_requests(self):
        """Process requests from the bucket based on leak rate."""
        current_time = time.time()
        elapsed = current_time - self.last_leak
        
        # Calculate how many requests can be processed
        requests_to_process = int(elapsed * self.leak_rate)
        
        if requests_to_process > 0:
            # Remove processed requests from the front of the queue
            for _ in range(min(requests_to_process, len(self.queue))):
                if self.queue:
                    self.queue.popleft()
            self.last_leak = current_time
    
    def add_request(self) -> bool:
        """
        Try to add a request to the bucket.
        
        Returns:
            True if request was added, False if bucket is full
        """
        with self.lock:
            self._leak_requests()
            
            if len(self.queue) < self.capacity:
                self.queue.append(time.time())
                return True
            return False
    
    def get_queue_size(self) -> int:
        """
        Get the current number of requests in the bucket.
        
        Returns:
            Current queue size
        """
        with self.lock:
            self._leak_requests()
            return len(self.queue)
    
    def get_wait_time(self) -> float:
        """
        Calculate time to wait before a request can be added.
        
        Returns:
            Seconds to wait (0 if bucket has space)
        """
        with self.lock:
            self._leak_requests()
            
            if len(self.queue) < self.capacity:
                return 0.0
            
            # Calculate when the oldest request will be processed
            if self.queue:
                oldest_request = self.queue[0]
                requests_ahead = len(self.queue)
                time_to_process = requests_ahead / self.leak_rate
                return max(0.0, time_to_process)
            
            return 0.0
    
    def get_oldest_request_age(self) -> float:
        """
        Get the age of the oldest request in the bucket.
        
        Returns:
            Age in seconds (0 if bucket is empty)
        """
        with self.lock:
            if not self.queue:
                return 0.0
            return time.time() - self.queue[0]


class LeakyBucketRateLimiter:
    """
    Rate limiter using Leaky Bucket algorithm.
    Provides a simple interface for rate limiting requests.
    """
    
    def __init__(self, requests_per_second: float, bucket_size: Optional[int] = None):
        """
        Initialize rate limiter.
        
        Args:
            requests_per_second: Maximum requests per second (leak rate)
            bucket_size: Maximum bucket size (defaults to requests_per_second * 2)
        """
        size = bucket_size if bucket_size is not None else int(requests_per_second * 2)
        self.bucket = LeakyBucket(
            capacity=size,
            leak_rate=requests_per_second,
            initial_size=0
        )
    
    def allow_request(self) -> bool:
        """
        Check if a request should be allowed.
        
        Returns:
            True if request is allowed, False otherwise
        """
        return self.bucket.add_request()
    
    def get_status(self) -> dict:
        """
        Get current status of the rate limiter.
        
        Returns:
            Dictionary with status information
        """
        queue_size = self.bucket.get_queue_size()
        wait_time = self.bucket.get_wait_time()
        oldest_age = self.bucket.get_oldest_request_age()
        
        return {
            "queue_size": queue_size,
            "capacity": self.bucket.capacity,
            "leak_rate": self.bucket.leak_rate,
            "wait_time_seconds": wait_time,
            "oldest_request_age_seconds": oldest_age,
            "available_space": self.bucket.capacity - queue_size
        }


# Example usage and testing
if __name__ == "__main__":
    print("=" * 60)
    print("Leaky Bucket Rate Limiting Algorithm - Demo")
    print("=" * 60)
    print()
    
    # Create a rate limiter: 5 requests per second, bucket size of 10
    limiter = LeakyBucketRateLimiter(requests_per_second=5.0, bucket_size=10)
    
    print("Configuration:")
    print(f"  - Requests per second: 5.0")
    print(f"  - Bucket size: 10")
    print()
    
    # Test 1: Fill bucket
    print("Test 1: Fill Bucket (15 requests)")
    print("-" * 60)
    allowed = 0
    denied = 0
    
    for i in range(15):
        if limiter.allow_request():
            allowed += 1
            status = limiter.get_status()
            print(f"Request {i+1}: ✅ Allowed (Queue: {status['queue_size']}/{status['capacity']})")
        else:
            denied += 1
            status = limiter.get_status()
            print(f"Request {i+1}: ❌ Denied (Queue: {status['queue_size']}/{status['capacity']}, Wait: {status['wait_time_seconds']:.2f}s)")
    
    print(f"\nResults: {allowed} allowed, {denied} denied")
    print()
    
    # Test 2: Wait and retry
    print("Test 2: Wait for Bucket to Leak (wait 2 seconds)")
    print("-" * 60)
    time.sleep(2)
    
    status = limiter.get_status()
    print(f"After waiting: Queue size = {status['queue_size']}/{status['capacity']}")
    print(f"Oldest request age: {status['oldest_request_age_seconds']:.2f} seconds")
    print()
    
    # Test 3: Steady rate
    print("Test 3: Steady Rate (10 requests with 0.2s delay)")
    print("-" * 60)
    allowed = 0
    denied = 0
    
    for i in range(10):
        if limiter.allow_request():
            allowed += 1
            status = limiter.get_status()
            print(f"Request {i+1}: ✅ Allowed (Queue: {status['queue_size']}/{status['capacity']})")
        else:
            denied += 1
            print(f"Request {i+1}: ❌ Denied")
        time.sleep(0.2)  # 0.2s = 5 requests per second
    
    print(f"\nResults: {allowed} allowed, {denied} denied")
    print()
    
    # Test 4: Status check
    print("Test 4: Status Check")
    print("-" * 60)
    status = limiter.get_status()
    print(f"Queue size: {status['queue_size']}/{status['capacity']}")
    print(f"Available space: {status['available_space']}")
    print(f"Leak rate: {status['leak_rate']} requests/second")
    print(f"Wait time for next slot: {status['wait_time_seconds']:.2f} seconds")
    print(f"Oldest request age: {status['oldest_request_age_seconds']:.2f} seconds")
    print()
    
    print("✅ Leaky Bucket algorithm demonstration complete!")

