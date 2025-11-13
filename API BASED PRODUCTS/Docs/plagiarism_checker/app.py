import streamlit as st
import joblib
from utils import calculate_cosine_similarity, highlight_matching_text
import os

# Load model
try:
    model = joblib.load("plagiarism_model.pkl")
except FileNotFoundError:
    st.error("Model not found! Please run model.py first to train the model.")
    st.stop()

st.set_page_config(page_title="Plagiarism Checker", layout="wide")

st.title("📄 Plagiarism Checker")
st.markdown("Upload two text files to check for plagiarism using Cosine Similarity and ML Classification")

# File upload
col1, col2 = st.columns(2)

with col1:
    file1 = st.file_uploader("Upload Original File", type=["txt"])

with col2:
    file2 = st.file_uploader("Upload Submission File", type=["txt"])

if file1 and file2:
    text1 = file1.read().decode("utf-8")
    text2 = file2.read().decode("utf-8")
    
    # Calculate similarity
    similarity = calculate_cosine_similarity(text1, text2)
    
    # ML prediction
    prediction = model.predict([[similarity]])[0]
    prob = model.predict_proba([[similarity]])[0][1]
    
    # Display results
    st.markdown("---")
    st.subheader("📊 Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Cosine Similarity Score", f"{similarity:.4f}")
    
    with col2:
        st.metric("Plagiarism Probability", f"{prob:.4f}")
    
    with col3:
        if prediction == 1:
            st.error("🔴 Plagiarized")
        else:
            st.success("🟢 Original")
    
    # Highlighted Text Display
    st.markdown("---")
    st.subheader("📌 Highlighted Matching Text")
    
    highlighted1, highlighted2 = highlight_matching_text(text1, text2)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Original File (Highlighted):**", unsafe_allow_html=True)
        st.markdown(
            f"<div style='background-color:#f9f9f9;padding:15px;border-radius:8px;border:1px solid #ddd;max-height:400px;overflow-y:auto'>{highlighted1}</div>", 
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown("**Submission File (Highlighted):**", unsafe_allow_html=True)
        st.markdown(
            f"<div style='background-color:#f0f0f0;padding:15px;border-radius:8px;border:1px solid #ddd;max-height:400px;overflow-y:auto'>{highlighted2}</div>", 
            unsafe_allow_html=True
        )
    
    # Additional info
    st.markdown("---")
    with st.expander("ℹ️ How it works"):
        st.markdown("""
        **Plagiarism Detection Process:**
        1. **TF-IDF Vectorization**: Both documents are converted to TF-IDF vectors
        2. **Cosine Similarity**: Measures the similarity between the two vectors (0-1 scale)
        3. **ML Classification**: A trained Logistic Regression model classifies based on similarity threshold
        4. **Text Highlighting**: Matching segments are highlighted using sequence matching algorithms
        
        **Interpretation:**
        - Similarity Score: 0.0 (completely different) to 1.0 (identical)
        - Plagiarism Probability: Likelihood that the submission is plagiarized
        - Highlighted Text: Yellow highlights show matching segments between documents
        """)

