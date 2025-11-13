# Question 3: Rate Limiting Algorithms Implementation

This directory contains implementations of two classic rate limiting algorithms:
1. **Token Bucket Algorithm**
2. **Leaky Bucket Algorithm**

Both implementations are in Python with thread-safe operations and comprehensive testing.

## 📋 Files

- `token_bucket.py` - Token Bucket algorithm implementation
- `leaky_bucket.py` - Leaky Bucket algorithm implementation
- `comparison_demo.py` - Side-by-side comparison of both algorithms
- `README.md` - This file

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- No external dependencies (uses only standard library)

### Running the Demos

**Token Bucket Demo:**
```bash
python token_bucket.py
```

**Leaky Bucket Demo:**
```bash
python leaky_bucket.py
```

**Comparison Demo:**
```bash
python comparison_demo.py
```

## 📖 Algorithm Details

### Token Bucket Algorithm

**How it works:**
- Maintains a bucket with a maximum capacity of tokens
- Tokens are added to the bucket at a constant rate (refill rate)
- When a request arrives, it consumes a token
- If tokens are available, the request is allowed; otherwise, it's rejected
- Tokens accumulate up to the bucket capacity when not used

**Key Features:**
- ✅ Allows bursts up to bucket capacity
- ✅ Tokens accumulate when traffic is low
- ✅ Flexible for variable traffic patterns
- ✅ Good for handling traffic spikes

**Use Cases:**
- API rate limiting with burst allowance
- Network traffic shaping
- Resource allocation systems

**Example:**
```python
from token_bucket import TokenBucketRateLimiter

# Create limiter: 5 requests/second, burst of 10
limiter = TokenBucketRateLimiter(requests_per_second=5.0, burst_size=10)

# Check if request is allowed
if limiter.allow_request():
    # Process request
    pass
else:
    # Reject request
    pass
```

### Leaky Bucket Algorithm

**How it works:**
- Maintains a bucket (queue) with a maximum capacity
- Requests are added to the bucket
- The bucket "leaks" at a constant rate, processing requests
- If the bucket is full, new requests are rejected
- Requests are processed in FIFO order

**Key Features:**
- ✅ Maintains constant output rate
- ✅ Smooths out traffic bursts
- ✅ No accumulation of capacity
- ✅ Predictable processing rate

**Use Cases:**
- Network traffic shaping with constant rate
- Request queuing systems
- Systems requiring smooth output rate

**Example:**
```python
from leaky_bucket import LeakyBucketRateLimiter

# Create limiter: 5 requests/second, bucket size 10
limiter = LeakyBucketRateLimiter(requests_per_second=5.0, bucket_size=10)

# Check if request is allowed
if limiter.allow_request():
    # Process request
    pass
else:
    # Reject request
    pass
```

## 🔍 Comparison

| Feature | Token Bucket | Leaky Bucket |
|---------|-------------|--------------|
| **Burst Handling** | ✅ Allows bursts | ❌ Smooths bursts |
| **Token Accumulation** | ✅ Yes | ❌ No |
| **Output Rate** | Variable | Constant |
| **Complexity** | Medium | Medium |
| **Best For** | Variable traffic | Constant rate |

## 🧪 Testing

Both implementations include comprehensive test cases:

1. **Burst Requests Test** - Tests handling of sudden traffic spikes
2. **Steady Rate Test** - Tests handling of constant rate traffic
3. **Status Check** - Tests status reporting functionality

## 📊 Output Examples

### Token Bucket Output
```
Token Bucket Rate Limiting Algorithm - Demo
============================================================

Configuration:
  - Requests per second: 5.0
  - Burst size: 10

Test 1: Burst Requests (15 requests)
------------------------------------------------------------
Request 1: ✅ Allowed
Request 2: ✅ Allowed
...
Request 11: ❌ Denied

Results: 10 allowed, 5 denied
```

### Leaky Bucket Output
```
Leaky Bucket Rate Limiting Algorithm - Demo
============================================================

Configuration:
  - Requests per second: 5.0
  - Bucket size: 10

Test 1: Fill Bucket (15 requests)
------------------------------------------------------------
Request 1: ✅ Allowed (Queue: 1/10)
Request 2: ✅ Allowed (Queue: 2/10)
...
Request 11: ❌ Denied (Queue: 10/10, Wait: 2.00s)

Results: 10 allowed, 5 denied
```

## 🔧 Advanced Usage

### Custom Configuration

**Token Bucket:**
```python
from token_bucket import TokenBucket

bucket = TokenBucket(
    capacity=20,           # Max tokens
    refill_rate=10.0,      # Tokens per second
    initial_tokens=20      # Start with full bucket
)

# Consume multiple tokens
if bucket.consume(tokens=3):
    # Process request requiring 3 tokens
    pass
```

**Leaky Bucket:**
```python
from leaky_bucket import LeakyBucket

bucket = LeakyBucket(
    capacity=20,           # Max requests
    leak_rate=10.0,        # Requests per second
    initial_size=5         # Start with 5 requests
)

# Check wait time
wait_time = bucket.get_wait_time()
if wait_time > 0:
    print(f"Wait {wait_time:.2f} seconds")
```

### Thread-Safe Operations

Both implementations are thread-safe and can be used in multi-threaded environments:

```python
import threading
from token_bucket import TokenBucketRateLimiter

limiter = TokenBucketRateLimiter(requests_per_second=10.0)

def worker():
    for _ in range(100):
        if limiter.allow_request():
            # Process request
            pass

# Create multiple threads
threads = [threading.Thread(target=worker) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

## 📝 Notes

- Both algorithms use `threading.Lock()` for thread safety
- Time-based calculations use `time.time()` for precision
- Token Bucket allows bursts up to capacity
- Leaky Bucket maintains constant output rate
- Both algorithms are suitable for production use with proper testing

## 🎯 Assignment Deliverables

1. ✅ Token Bucket implementation (`token_bucket.py`)
2. ✅ Leaky Bucket implementation (`leaky_bucket.py`)
3. ✅ Comparison demo (`comparison_demo.py`)
4. ✅ Comprehensive documentation (this README)
5. ✅ Test cases and examples included in each file

## 📸 Screenshots for Assignment

When demonstrating, capture:
1. Token Bucket demo output showing burst handling
2. Leaky Bucket demo output showing queue management
3. Comparison demo showing differences
4. Code snippets from both implementations

