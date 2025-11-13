"""
Flask API for plagiarism detection.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import calculate_cosine_similarity, highlight_matching_text
import joblib
import os


app = Flask(__name__)
CORS(app)  # Enable CORS for Streamlit frontend

# Load model
model_path = "plagiarism_model.pkl"
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    raise FileNotFoundError(f"Model file '{model_path}' not found! Please run model.py first.")


@app.route("/", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "message": "Plagiarism Checker API is running"})


@app.route("/check", methods=["POST"])
def check():
    """
    Check plagiarism between two uploaded text files.
    
    Expected form data:
    - original: File object (text file)
    - submission: File object (text file)
    
    Returns:
        JSON response with similarity score, prediction, probability, and highlighted text
    """
    try:
        if 'original' not in request.files or 'submission' not in request.files:
            return jsonify({"error": "Both 'original' and 'submission' files are required"}), 400
        
        file1 = request.files['original']
        file2 = request.files['submission']
        
        if file1.filename == '' or file2.filename == '':
            return jsonify({"error": "Both files must be selected"}), 400
        
        text1 = file1.read().decode("utf-8")
        text2 = file2.read().decode("utf-8")
        
        # Calculate similarity
        similarity = calculate_cosine_similarity(text1, text2)
        
        # Make prediction
        prediction = model.predict([[similarity]])[0]
        probability = model.predict_proba([[similarity]])[0][1]
        
        # Get highlighted text
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
    print("Starting Flask API server on http://localhost:5000")
    app.run(debug=True, port=5000, host='0.0.0.0')

