from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import calculate_cosine_similarity, highlight_matching_text
import joblib
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for Streamlit frontend

# Load model
try:
    model = joblib.load("plagiarism_model.pkl")
    print("Model loaded successfully!")
except FileNotFoundError:
    print("Warning: Model not found! Please run model.py first to train the model.")
    model = None


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Plagiarism Checker API",
        "endpoints": {
            "/check": "POST - Check plagiarism between two text files",
            "/health": "GET - Health check"
        }
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None
    })


@app.route("/check", methods=["POST"])
def check():
    """
    Check plagiarism between two uploaded text files.
    
    Expected form data:
    - original: File object (text file)
    - submission: File object (text file)
    
    Returns:
    JSON response with similarity score, prediction, and highlighted text
    """
    if model is None:
        return jsonify({"error": "Model not loaded. Please train the model first."}), 500
    
    if 'original' not in request.files or 'submission' not in request.files:
        return jsonify({"error": "Both 'original' and 'submission' files are required"}), 400
    
    try:
        file1 = request.files['original']
        file2 = request.files['submission']
        
        text1 = file1.read().decode("utf-8")
        text2 = file2.read().decode("utf-8")
        
        # Calculate similarity
        similarity = calculate_cosine_similarity(text1, text2)
        
        # ML prediction
        prediction = model.predict([[similarity]])[0]
        probability = model.predict_proba([[similarity]])[0][1]
        
        # Highlight matching text
        highlight1, highlight2 = highlight_matching_text(text1, text2)
        
        return jsonify({
            "similarity_score": round(similarity, 4),
            "plagiarized": bool(prediction),
            "probability": round(probability, 4),
            "highlighted_original": highlight1,
            "highlighted_submission": highlight2
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("Starting Flask API server...")
    print("API will be available at http://localhost:5000")
    app.run(debug=True, port=5000, host='0.0.0.0')

