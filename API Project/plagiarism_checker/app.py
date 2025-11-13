"""
Streamlit web application for plagiarism detection.
"""
import streamlit as st
import joblib
from utils import calculate_cosine_similarity, highlight_matching_text
import os


# Load model
if os.path.exists("plagiarism_model.pkl"):
    model = joblib.load("plagiarism_model.pkl")
else:
    st.error("Model file not found! Please run model.py first to train the model.")
    st.stop()

st.title("📄 Plagiarism Checker")
st.markdown("Upload two text files to check for plagiarism using cosine similarity and ML classification.")

# File upload
file1 = st.file_uploader("Upload Original File", type=["txt"])
file2 = st.file_uploader("Upload Submission File", type=["txt"])

if file1 and file2:
    text1 = file1.read().decode("utf-8")
    text2 = file2.read().decode("utf-8")
    
    # Calculate similarity
    similarity = calculate_cosine_similarity(text1, text2)
    
    # Make prediction
    prediction = model.predict([[similarity]])[0]
    prob = model.predict_proba([[similarity]])[0][1]

    # Display results
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Cosine Similarity Score", f"{similarity:.4f}")
    with col2:
        st.metric("Plagiarism Probability", f"{prob:.4f}")
    
    if prediction == 1:
        st.error("🔴 This submission is likely plagiarized.")
    else:
        st.success("🟢 This submission seems original.")
    
    # Highlighted Text Display
    st.subheader("📌 Highlighted Matching Text")
    highlighted1, highlighted2 = highlight_matching_text(text1, text2)
    
    st.markdown("**Original File (Highlighted):**", unsafe_allow_html=True)
    st.markdown(
        f"<div style='background-color:#f9f9f9;padding:15px;border-radius:8px;border:1px solid #ddd;max-height:300px;overflow-y:auto'>{highlighted1}</div>", 
        unsafe_allow_html=True
    )
    
    st.markdown("**Submission File (Highlighted):**", unsafe_allow_html=True)
    st.markdown(
        f"<div style='background-color:#f0f0f0;padding:15px;border-radius:8px;border:1px solid #ddd;max-height:300px;overflow-y:auto'>{highlighted2}</div>", 
        unsafe_allow_html=True
    )
    
    # Show raw text in expander
    with st.expander("View Raw Text"):
        col1, col2 = st.columns(2)
        with col1:
            st.text_area("Original Text", text1, height=200, key="original_raw")
        with col2:
            st.text_area("Submission Text", text2, height=200, key="submission_raw")

