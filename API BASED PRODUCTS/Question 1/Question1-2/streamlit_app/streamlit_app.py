import streamlit as st
import joblib
from utils import calculate_cosine_similarity, highlight_matching_text
import os

# Page configuration
st.set_page_config(
    page_title="Plagiarism Checker",
    page_icon="📄",
    layout="wide"
)

# Load model
@st.cache_resource
def load_model():
    if not os.path.exists("plagiarism_model.pkl"):
        st.error("Model file not found! Please run model.py first to train the model.")
        st.stop()
    return joblib.load("plagiarism_model.pkl")

model = load_model()

# Title and description
st.title("📄 Plagiarism Checker")
st.markdown("""
This application uses **Machine Learning** and **Cosine Similarity** to detect plagiarism.
Upload two text files to check if the submission is plagiarized from the original.
""")

# Add sidebar with information
with st.sidebar:
    st.header("ℹ️ How it works")
    st.markdown("""
    1. **TF-IDF Vectorization**: Converts text to numerical vectors
    2. **Cosine Similarity**: Measures similarity between documents
    3. **ML Classification**: Uses Logistic Regression to classify
    4. **Highlighting**: Shows matching text segments
    """)
    st.markdown("---")
    st.markdown("**Threshold**: Similarity ≥ 80% indicates plagiarism")

# Create two columns for file upload
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Original Document")
    file1 = st.file_uploader("Upload Original File", type=["txt"], key="file1")

with col2:
    st.subheader("📝 Submission Document")
    file2 = st.file_uploader("Upload Submission File", type=["txt"], key="file2")

# Process files when both are uploaded
if file1 and file2:
    # Read file contents
    text1 = file1.read().decode("utf-8")
    text2 = file2.read().decode("utf-8")
    
    # Calculate similarity
    similarity = calculate_cosine_similarity(text1, text2)
    
    # Make prediction
    prediction = model.predict([[similarity]])[0]
    prob = model.predict_proba([[similarity]])[0][1]
    
    # Display results in a nice format
    st.markdown("---")
    st.header("📊 Results")
    
    # Create metrics row
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    with metric_col1:
        st.metric(
            label="Cosine Similarity Score",
            value=f"{similarity:.2%}",
            delta=f"{abs(similarity - 0.8):.2%} from threshold"
        )
    
    with metric_col2:
        st.metric(
            label="Plagiarism Probability",
            value=f"{prob:.2%}"
        )
    
    with metric_col3:
        if prediction == 1:
            st.error("🔴 **PLAGIARIZED**")
        else:
            st.success("🟢 **ORIGINAL**")
    
    # Detailed verdict
    st.markdown("---")
    if prediction == 1:
        st.error("""
        ### ⚠️ Plagiarism Detected
        This submission is likely plagiarized from the original document.
        The similarity score exceeds the threshold, and the ML model confirms plagiarism.
        """)
    else:
        st.success("""
        ### ✅ Original Content
        This submission appears to be original content.
        The similarity score is below the threshold, indicating independent work.
        """)
    
    # Highlighted Text Display
    st.markdown("---")
    st.header("🔍 Highlighted Matching Segments")
    st.markdown("Matching text segments are highlighted in **yellow**.")
    
    # Get highlighted versions
    highlighted1, highlighted2 = highlight_matching_text(text1, text2)
    
    # Display in two columns
    highlight_col1, highlight_col2 = st.columns(2)
    
    with highlight_col1:
        st.markdown("**📄 Original File (Highlighted):**")
        st.markdown(
            f"<div style='background-color:#f9f9f9;padding:15px;border-radius:8px;border:1px solid #ddd;max-height:400px;overflow-y:auto;'>{highlighted1}</div>",
            unsafe_allow_html=True
        )
    
    with highlight_col2:
        st.markdown("**📝 Submission File (Highlighted):**")
        st.markdown(
            f"<div style='background-color:#f0f0f0;padding:15px;border-radius:8px;border:1px solid #ddd;max-height:400px;overflow-y:auto;'>{highlighted2}</div>",
            unsafe_allow_html=True
        )
    
    # Statistics
    st.markdown("---")
    st.header("📈 Document Statistics")
    stat_col1, stat_col2 = st.columns(2)
    
    with stat_col1:
        st.info(f"""
        **Original Document:**
        - Characters: {len(text1)}
        - Words: {len(text1.split())}
        - Lines: {len(text1.splitlines())}
        """)
    
    with stat_col2:
        st.info(f"""
        **Submission Document:**
        - Characters: {len(text2)}
        - Words: {len(text2.split())}
        - Lines: {len(text2.splitlines())}
        """)

else:
    # Show instructions when files are not uploaded
    st.info("👆 Please upload both files to start the plagiarism check.")
    
    # Show example
    with st.expander("📝 See Example"):
        st.markdown("""
        **Sample Original Text:**
        ```
        Machine learning is a subset of artificial intelligence that focuses on 
        building systems that can learn from and make decisions based on data.
        ```
        
        **Sample Plagiarized Submission:**
        ```
        Machine learning is a subset of artificial intelligence that focuses on 
        creating systems that learn from data and make decisions accordingly.
        ```
        
        **Expected Result:** High similarity score, plagiarism detected
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Built with Streamlit | Uses TF-IDF + Cosine Similarity + Logistic Regression</p>
</div>
""", unsafe_allow_html=True)