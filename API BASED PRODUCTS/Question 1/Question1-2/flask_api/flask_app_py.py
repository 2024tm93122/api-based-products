from flask import Flask, request, jsonify
from utils import calculate_cosine_similarity, highlight_matching_text
import joblib
import os

app = Flask(__name__)

# Load the trained model
model = joblib.load("plagiarism_model.pkl")

@app.route('/')
def home():
    """API home endpoint with documentation"""
    return jsonify({
        "message": "Plagiarism Checker API",
        "version": "1.0",
        "endpoints": {
            "/check": {
                "method": "POST",
                "description": "Check plagiarism between two text files",
                "parameters": {
                    "original": "Original text file (multipart/form-data)",
                    "submission": "Submission text file (multipart/form-data)"
                },
                "returns": {
                    "similarity_score": "Cosine similarity score (0-1)",
                    "plagiarized": "Boolean indicating if content is plagiarized",
                    "probability": "Probability of plagiarism (0-1)",
                    "highlighted_original": "Original text with matches highlighted",
                    "highlighted_submission": "Submission text with matches highlighted"
                }
            },
            "/health": {
                "method": "GET",
                "description": "Health check endpoint"
            }
        }
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model_loaded": True
    })

@app.route('/check', methods=['POST'])
def check():
    """Main endpoint to check plagiarism"""
    try:
        # Check if files are present
        if 'original' not in request.files or 'submission' not in request.files:
            return jsonify({
                "error": "Both 'original' and 'submission' files are required"
            }), 400
        
        # Get uploaded files
        file1 = request.files['original']
        file2 = request.files['submission']
        
        # Check if files are empty
        if file1.filename == '' or file2.filename == '':
            return jsonify({
                "error": "No file selected"
            }), 400
        
        # Read file contents
        text1 = file1.read().decode("utf-8")
        text2 = file2.read().decode("utf-8")
        
        # Validate content
        if not text1.strip() or not text2.strip():
            return jsonify({
                "error": "Files cannot be empty"
            }), 400
        
        # Calculate similarity
        similarity = calculate_cosine_similarity(text1, text2)
        
        # Make prediction
        prediction = model.predict([[similarity]])[0]
        probability = model.predict_proba([[similarity]])[0][1]
        
        # Get highlighted text
        highlight1, highlight2 = highlight_matching_text(text1, text2)
        
        # Return results
        return jsonify({
            "similarity_score": round(similarity, 4),
            "plagiarized": bool(prediction),
            "probability": round(probability, 4),
            "highlighted_original": highlight1,
            "highlighted_submission": highlight2,
            "metadata": {
                "original_length": len(text1),
                "submission_length": len(text2),
                "original_words": len(text1.split()),
                "submission_words": len(text2.split())
            }
        })
    
    except Exception as e:
        return jsonify({
            "error": f"An error occurred: {str(e)}"
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "message": "Please refer to the API documentation at /"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "message": str(error)
    }), 500

if __name__ == "__main__":
    # Check if model exists
    if not os.path.exists("plagiarism_model.pkl"):
        print("ERROR: Model file not found!")
        print("Please run model.py first to train the model.")
        exit(1)
    
    print("=" * 50)
    print("Plagiarism Checker API")
    print("=" * 50)
    print("API is running on: http://localhost:5000")
    print("Endpoints:")
    print("  GET  /           - API documentation")
    print("  GET  /health     - Health check")
    print("  POST /check      - Check plagiarism")
    print("=" * 50)
    
    app.run(debug=True, port=5000)
