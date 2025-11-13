import streamlit as st
import requests

st.set_page_config(page_title="Plagiarism Checker", layout="wide")

st.title("📄 Plagiarism Checker")
st.markdown("Upload original and submitted text files to check for plagiarism using Flask API backend.")

# API endpoint configuration
api_url = st.sidebar.text_input("API URL", value="http://localhost:5000")

# Health check
try:
    health_response = requests.get(f"{api_url}/health", timeout=2)
    if health_response.status_code == 200:
        st.sidebar.success("✅ API Connected")
    else:
        st.sidebar.warning("⚠️ API may not be ready")
except:
    st.sidebar.error("❌ API Not Connected")
    st.sidebar.info("Make sure Flask API is running on port 5000")

st.markdown("---")

# File upload
col1, col2 = st.columns(2)

with col1:
    original_file = st.file_uploader("Upload Original File", type=["txt"])

with col2:
    submission_file = st.file_uploader("Upload Submission File", type=["txt"])

if st.button("🔍 Check Plagiarism", type="primary") and original_file and submission_file:
    with st.spinner("Checking for plagiarism..."):
        try:
            files = {
                "original": (original_file.name, original_file.read(), "text/plain"),
                "submission": (submission_file.name, submission_file.read(), "text/plain")
            }
            
            # Reset file pointers
            original_file.seek(0)
            submission_file.seek(0)
            
            response = requests.post(f"{api_url}/check", files=files, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                st.markdown("---")
                st.subheader("📊 Results")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Similarity Score", f"{data['similarity_score'] * 100:.2f}%")
                
                with col2:
                    st.metric("Plagiarism Probability", f"{data['probability'] * 100:.2f}%")
                
                with col3:
                    if data["plagiarized"]:
                        st.error("🔴 Plagiarized")
                    else:
                        st.success("🟢 Original")
                
                # Highlighted Text Display
                st.markdown("---")
                st.subheader("📌 Highlighted Matching Text")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Original File (Highlighted):**", unsafe_allow_html=True)
                    st.markdown(
                        f"<div style='background-color:#f9f9f9;padding:15px;border-radius:8px;border:1px solid #ddd;max-height:400px;overflow-y:auto'>{data['highlighted_original']}</div>", 
                        unsafe_allow_html=True
                    )
                
                with col2:
                    st.markdown("**Submission File (Highlighted):**", unsafe_allow_html=True)
                    st.markdown(
                        f"<div style='background-color:#f0f0f0;padding:15px;border-radius:8px;border:1px solid #ddd;max-height:400px;overflow-y:auto'>{data['highlighted_submission']}</div>", 
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
                    
                    **API Architecture:**
                    - **Backend**: Flask REST API handles the plagiarism detection logic
                    - **Frontend**: Streamlit provides the user interface
                    - **Communication**: HTTP POST requests with file uploads
                    """)
            
            else:
                error_data = response.json() if response.content else {}
                st.error(f"Error from API: {error_data.get('error', 'Unknown error')}")
        
        except requests.exceptions.ConnectionError:
            st.error("❌ Connection failed! Make sure the Flask API is running.")
            st.info("To start the API, run: `python flask_api/app.py`")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")

elif original_file and submission_file:
    st.info("👆 Click the 'Check Plagiarism' button to analyze the files")

