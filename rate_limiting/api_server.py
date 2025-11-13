"""
Flask API Server with Rate Limiting

Demonstrates Token Bucket and Leaky Bucket rate limiting in a web API context.
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from token_bucket import TokenBucketRateLimiter
from leaky_bucket import LeakyBucketRateLimiter
import time

app = Flask(__name__)
CORS(app)

# Initialize rate limiters
# Capacity: 10 requests, Rate: 5 requests per second
token_bucket_limiter = TokenBucketRateLimiter(capacity=10, refill_rate=5.0)
leaky_bucket_limiter = LeakyBucketRateLimiter(capacity=10, leak_rate=5.0)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Rate Limiting API Server",
        "endpoints": {
            "/api/token-bucket": "GET - Test Token Bucket rate limiting",
            "/api/leaky-bucket": "GET - Test Leaky Bucket rate limiting",
            "/api/stats": "GET - Get rate limiter statistics"
        }
    })


@app.route("/api/token-bucket", methods=["GET"])
def token_bucket_endpoint():
    """Endpoint protected by Token Bucket rate limiting."""
    allowed, wait_time = token_bucket_limiter.allow_request()
    
    if allowed:
        return jsonify({
            "status": "success",
            "message": "Request allowed",
            "algorithm": "Token Bucket",
            "available_tokens": round(token_bucket_limiter.bucket.get_available_tokens(), 2),
            "timestamp": time.time()
        }), 200
    else:
        return jsonify({
            "status": "rate_limited",
            "message": "Rate limit exceeded",
            "algorithm": "Token Bucket",
            "wait_time_seconds": round(wait_time, 2),
            "retry_after": round(wait_time, 2),
            "timestamp": time.time()
        }), 429


@app.route("/api/leaky-bucket", methods=["GET"])
def leaky_bucket_endpoint():
    """Endpoint protected by Leaky Bucket rate limiting."""
    allowed, wait_time = leaky_bucket_limiter.allow_request()
    
    if allowed:
        return jsonify({
            "status": "success",
            "message": "Request allowed",
            "algorithm": "Leaky Bucket",
            "queue_size": leaky_bucket_limiter.bucket.get_queue_size(),
            "timestamp": time.time()
        }), 200
    else:
        return jsonify({
            "status": "rate_limited",
            "message": "Rate limit exceeded",
            "algorithm": "Leaky Bucket",
            "wait_time_seconds": round(wait_time, 2),
            "retry_after": round(wait_time, 2),
            "timestamp": time.time()
        }), 429


@app.route("/api/stats", methods=["GET"])
def stats():
    """Get statistics for both rate limiters."""
    return jsonify({
        "token_bucket": {
            "available_tokens": round(token_bucket_limiter.bucket.get_available_tokens(), 2),
            "capacity": token_bucket_limiter.bucket.capacity,
            "refill_rate": token_bucket_limiter.bucket.refill_rate
        },
        "leaky_bucket": {
            "queue_size": leaky_bucket_limiter.bucket.get_queue_size(),
            "capacity": leaky_bucket_limiter.bucket.capacity,
            "leak_rate": leaky_bucket_limiter.bucket.leak_rate
        }
    }), 200


@app.route("/api/reset", methods=["POST"])
def reset():
    """Reset both rate limiters (for testing purposes)."""
    token_bucket_limiter.bucket.reset()
    leaky_bucket_limiter.bucket.reset()
    return jsonify({
        "message": "Rate limiters reset",
        "timestamp": time.time()
    }), 200


if __name__ == "__main__":
    print("Starting Rate Limiting API Server...")
    print("Endpoints:")
    print("  GET  http://localhost:5001/api/token-bucket")
    print("  GET  http://localhost:5001/api/leaky-bucket")
    print("  GET  http://localhost:5001/api/stats")
    print("  POST http://localhost:5001/api/reset")
    app.run(host="0.0.0.0", port=5001, debug=True)

