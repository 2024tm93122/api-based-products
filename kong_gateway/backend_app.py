from flask import Flask, jsonify, request
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Backend Service",
        "timestamp": time.time(),
        "status": "running"
    })

@app.route("/api/data", methods=["GET", "POST"])
def data():
    if request.method == "GET":
        return jsonify({
            "message": "GET request successful",
            "data": {"key": "value"},
            "timestamp": time.time()
        })
    elif request.method == "POST":
        return jsonify({
            "message": "POST request successful",
            "received_data": request.json if request.is_json else request.form.to_dict(),
            "timestamp": time.time()
        })

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "backend-service"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

