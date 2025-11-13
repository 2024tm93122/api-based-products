"""
Leaky Bucket Rate Limiting Algorithm

Concept:
- A bucket holds requests with a maximum capacity
- Requests "leak" out at a constant rate
- New requests are added to the bucket
- If bucket is full, new requests are rejected
- Smooths out burst traffic to constant rate

Use Case: Network packet scheduling, traffic smoothing
"""

import time
import threading
from collections import deque
from typing import Optional


class LeakyBucket:
    """
    Leaky Bucket implementation for rate limiting.
    
    Args:
        capacity: Maximum number of requests bucket can hold
        leak_rate: Number of requests processed per second
    """
    
    def __init__(self, capacity: int, leak_rate: float):
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.queue = deque()
        self.last_leak_time = time.time()
        self.lock = threading.Lock()
    
    def _leak(self):
        """Process (leak) requests at constant rate"""
        now = time.time()
        elapsed = now - self.last_leak_time
        
        # Calculate how many requests should have leaked
        requests_to_leak = int(elapsed * self.leak_rate)
        
        if requests_to_leak > 0:
            # Remove leaked requests from queue
            for _ in range(min(requests_to_leak, len(self.queue))):
                self.queue.popleft()
            
            self.last_leak_time = now
    
    def add_request(self, request_id: str = None) -> bool:
        """
        Try to add a request to the bucket.
        
        Args:
            request_id: Optional identifier for the request
            
        Returns:
            True if request added, False if bucket is full
        """
        with self.lock:
            self._leak()
            
            if len(self.queue) < self.capacity:
                self.queue.append({
                    "id": request_id or f"req_{time.time()}",
                    "timestamp": time.time()
                })
                return True
            return False
    
    def get_queue_size(self) -> int:
        """Get current number of requests in queue"""
        with self.lock:
            self._leak()
            return len(self.queue)
    
    def get_wait_time(self) -> float:
        """Calculate wait time if bucket is full"""
        with self.lock:
            self._leak()
            
            if len(self.queue) < self.capacity:
                return 0.0
            
            # Time until one slot becomes available
            return 1.0 / self.leak_rate
    
    def is_full(self) -> bool:
        """Check if bucket is full"""
        with self.lock:
            self._leak()
            return len(self.queue) >= self.capacity


class LeakyBucketRateLimiter:
    """
    Rate limiter using Leaky Bucket algorithm.
    Manages multiple buckets for different clients.
    """
    
    def __init__(self, capacity: int, leak_rate: float):
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.buckets = {}
        self.lock = threading.Lock()
    
    def allow_request(self, client_id: str, request_id: str = None) -> tuple[bool, Optional[float]]:
        """
        Check if request is allowed for client.
        
        Args:
            client_id: Unique identifier for client
            request_id: Optional request identifier
            
        Returns:
            Tuple of (allowed: bool, retry_after: Optional[float])
        """
        with self.lock:
            if client_id not in self.buckets:
                self.buckets[client_id] = LeakyBucket(self.capacity, self.leak_rate)
        
        bucket = self.buckets[client_id]
        
        if bucket.add_request(request_id):
            return True, None
        else:
            retry_after = bucket.get_wait_time()
            return False, retry_after
    
    def get_client_info(self, client_id: str) -> dict:
        """Get information about client's bucket"""
        with self.lock:
            if client_id not in self.buckets:
                return {
                    "client_id": client_id,
                    "queue_size": 0,
                    "capacity": self.capacity,
                    "leak_rate": self.leak_rate,
                    "is_full": False
                }
            
            bucket = self.buckets[client_id]
            return {
                "client_id": client_id,
                "queue_size": bucket.get_queue_size(),
                "capacity": self.capacity,
                "leak_rate": self.leak_rate,
                "is_full": bucket.is_full()
            }


# ============================================================================
# DEMONSTRATION AND TESTING
# ============================================================================

def demonstrate_leaky_bucket():
    """Demonstrate Leaky Bucket algorithm"""
    
    print("=" * 70)
    print("LEAKY BUCKET RATE LIMITING ALGORITHM - DEMONSTRATION")
    print("=" * 70)
    
    # Create rate limiter: 10 capacity, 2 requests per second leak rate
    rate_limiter = LeakyBucketRateLimiter(capacity=10, leak_rate=2.0)
    
    print("\nConfiguration:")
    print(f"  - Bucket Capacity: 10 requests")
    print(f"  - Leak Rate: 2 requests/second")
    print(f"  - Initial State: Bucket is empty")
    
    # Test 1: Fill the bucket
    print("\n" + "=" * 70)
    print("Test 1: FILLING THE BUCKET (Testing capacity)")
    print("=" * 70)
    
    client_id = "user_123"
    
    for i in range(12):
        allowed, retry_after = rate_limiter.allow_request(client_id, f"req_{i+1}")
        info = rate_limiter.get_client_info(client_id)
        
        status = "✅ ADDED" if allowed else "❌ REJECTED"
        print(f"Request {i+1:2d}: {status} | Queue size: {info['queue_size']:2d}/{info['capacity']}")
        
        if not allowed:
            print(f"           → Bucket is full! Retry after: {retry_after:.2f}s")
    
    # Test 2: Leaking mechanism
    print("\n" + "=" * 70)
    print("Test 2: LEAKING MECHANISM (Observing constant leak rate)")
    print("=" * 70)
    print("Waiting for requests to leak out...")
    
    for i in range(6):
        time.sleep(1)
        info = rate_limiter.get_client_info(client_id)
        print(f"After {i+1}s: Queue size: {info['queue_size']:2d} (leaked ~{i+1*2} requests)")
    
    # Test 3: Burst followed by leak
    print("\n" + "=" * 70)
    print("Test 3: BURST + LEAK (Traffic smoothing)")
    print("=" * 70)
    
    client_id = "user_456"
    
    # Quick burst of requests
    print("Sending burst of 8 requests...")
    for i in range(8):
        allowed, _ = rate_limiter.allow_request(client_id, f"burst_{i+1}")
        info = rate_limiter.get_client_info(client_id)
        status = "✅" if allowed else "❌"
        print(f"  Request {i+1}: {status} | Queue: {info['queue_size']}")
    
    # Watch them leak out
    print("\nWatching requests leak out at constant rate...")
    for i in range(5):
        time.sleep(1)
        info = rate_limiter.get_client_info(client_id)
        print(f"After {i+1}s: Queue size: {info['queue_size']}")
    
    # Test 4: Multiple clients
    print("\n" + "=" * 70)
    print("Test 4: MULTIPLE CLIENTS (Independent buckets)")
    print("=" * 70)
    
    clients = ["client_A", "client_B", "client_C"]
    
    for client in clients:
        print(f"\n{client}:")
        for i in range(6):
            allowed, _ = rate_limiter.allow_request(client)
            info = rate_limiter.get_client_info(client)
            status = "✅" if allowed else "❌"
            print(f"  Request {i+1}: {status} | Queue: {info['queue_size']}/{info['capacity']}")
    
    # Test 5: Sustained load
    print("\n" + "=" * 70)
    print("Test 5: SUSTAINED LOAD (Matching leak rate)")
    print("=" * 70)
    
    client_id = "user_sustained"
    
    print("Sending requests at exactly the leak rate (2 req/s)...")
    print("This should maintain a stable queue size.\n")
    
    for i in range(10):
        allowed, _ = rate_limiter.allow_request(client_id)
        info = rate_limiter.get_client_info(client_id)
        status = "✅" if allowed else "❌"
        print(f"Request {i+1:2d}: {status} | Queue: {info['queue_size']:2d} | Time: {time.time():.2f}")
        
        time.sleep(0.5)  # 2 requests per second
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY: Leaky Bucket Characteristics")
    print("=" * 70)
    print("""
✓ Processes requests at constant rate (smoothing)
✓ Buffers burst traffic up to capacity
✓ Rejects requests when bucket is full
✓ Each client has independent bucket
✓ Predictable output rate
✓ No burst allowance after idle period

Use Cases:
- Network packet scheduling
- Traffic smoothing for downstream services
- Queue-based request processing
- Bandwidth limiting
    """)


def compare_token_vs_leaky_bucket():
    """Compare Token Bucket vs Leaky Bucket behavior"""
    
    print("\n" + "=" * 70)
    print("COMPARISON: Token Bucket vs Leaky Bucket")
    print("=" * 70)
    
    print("""
╔════════════════════════╦════════════════════════╦════════════════════════╗
║       Feature          ║    Token Bucket        ║    Leaky Bucket        ║
╠════════════════════════╬════════════════════════╬════════════════════════╣
║ Burst Handling         ║ Allows bursts up to    ║ Queues bursts, smooth  ║
║                        ║ bucket capacity        ║ output                 ║
╠════════════════════════╬════════════════════════╬════════════════════════╣
║ After Idle Period      ║ Bucket refills, allows ║ No burst allowance     ║
║                        ║ immediate burst        ║                        ║
╠════════════════════════╬════════════════════════╬════════════════════════╣
║ Output Rate            ║ Variable (bursty)      ║ Constant (smooth)      ║
╠════════════════════════╬════════════════════════╬════════════════════════╣
║ Queue/Buffer           ║ No queue               ║ Has request queue      ║
╠════════════════════════╬════════════════════════╬════════════════════════╣
║ Latency                ║ Immediate accept/reject║ May add queueing delay ║
╠════════════════════════╬════════════════════════╬════════════════════════╣
║ Best For               ║ API rate limiting      ║ Traffic shaping,       ║
║                        ║ User quotas            ║ network scheduling     ║
╚════════════════════════╩════════════════════════╩════════════════════════╝

Example Scenario:
- 10 requests sent in 1 second
- Rate limit: 2 requests/second
- Capacity/Queue: 5

Token Bucket:
  → First 5 requests: ✅ (consume available tokens)
  → Next 5 requests: ❌ (no tokens available)
  → After 2.5s: Can accept new requests (tokens refilled)

Leaky Bucket:
  → First 5 requests: ✅ (added to queue)
  → Next 5 requests: ❌ (queue full)
  → Processes at 2 req/s constant rate
  → Queue drains in 2.5 seconds
    """)


def simulate_network_traffic():
    """Simulate network traffic with leaky bucket"""
    
    print("\n" + "=" * 70)
    print("SIMULATED NETWORK TRAFFIC WITH LEAKY BUCKET")
    print("=" * 70)
    
    # Create network rate limiter: 100 packets queue, 50 packets/second
    network_limiter = LeakyBucketRateLimiter(capacity=100, leak_rate=50.0)
    
    print("\nNetwork Configuration:")
    print("  - Queue Capacity: 100 packets")
    print("  - Processing Rate: 50 packets/second")
    print("  - Simulating 200 packet burst\n")
    
    client = "network_interface_1"
    
    # Simulate burst
    accepted = 0
    rejected = 0
    
    for i in range(200):
        allowed, retry_after = network_limiter.allow_request(client, f"packet_{i+1}")
        
        if allowed:
            accepted += 1
        else:
            rejected += 1
    
    info = network_limiter.get_client_info(client)
    
    print(f"Burst Results:")
    print(f"  ✅ Accepted: {accepted} packets (queued)")
    print(f"  ❌ Rejected: {rejected} packets (dropped)")
    print(f"  📊 Queue size: {info['queue_size']}")
    print(f"  ⏱️  Queue will drain in: {info['queue_size'] / info['leak_rate']:.2f} seconds")
    
    # Watch queue drain
    print("\nQueue draining...")
    for i in range(3):
        time.sleep(1)
        info = network_limiter.get_client_info(client)
        print(f"  After {i+1}s: {info['queue_size']} packets remaining")


if __name__ == "__main__":
    # Run demonstration
    demonstrate_leaky_bucket()
    
    # Run comparison
    compare_token_vs_leaky_bucket()
    
    # Run network simulation
    simulate_network_traffic()
    
    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)
