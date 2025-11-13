"""
Streamlit frontend for Flask API plagiarism checker.
"""
import streamlit as st
import requests


st.title("📄 Plagiarism Checker (Flask API)")
st.markdown("Upload original and submitted text files to check for plagiarism using the Flask API backend.")


# API endpoint configuration
API_URL = st.sidebar.text_input("API URL", value="http://localhost:5000/check")

original_file = st.file_uploader("Upload Original File", type=["txt"])
submission_file = st.file_uploader("Upload Submission File", type=["txt"])


if st.button("Check Plagiarism") and original_file and submission_file:
    with st.spinner("Checking plagiarism..."):
        files = {
            "original": (original_file.name, original_file.read(), "text/plain"),
            "submission": (submission_file.name, submission_file.read(), "text/plain")
        }
        
        # Reset file pointers
        original_file.seek(0)
        submission_file.seek(0)
        
        try:
            response = requests.post(API_URL, files=files)
            
            if response.status_code == 200:
                data = response.json()
                
                # Display metrics
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Similarity Score", f"{data['similarity_score'] * 100:.2f}%")
                with col2:
                    st.metric("Plagiarism Probability", f"{data['probability'] * 100:.2f}%")
                
                # Display prediction
                if data["plagiarized"]:
                    st.error("🔴 Plagiarism Detected")
                else:
                    st.success("🟢 No Plagiarism Detected")
                
                # Display highlighted text
                st.markdown("### 🔍 Highlighted Matches in Original")
                st.markdown(
                    f"<div style='background-color:#f9f9f9;padding:15px;border-radius:8px;border:1px solid #ddd;max-height:300px;overflow-y:auto'>{data['highlighted_original']}</div>", 
                    unsafe_allow_html=True
                )
                
                st.markdown("### 🔍 Highlighted Matches in Submission")
                st.markdown(
                    f"<div style='background-color:#f0f0f0;padding:15px;border-radius:8px;border:1px solid #ddd;max-height:300px;overflow-y:auto'>{data['highlighted_submission']}</div>", 
                    unsafe_allow_html=True
                )
                
            else:
                st.error(f"Error from Flask API: {response.status_code}")
                try:
                    error_data = response.json()
                    st.error(f"Error message: {error_data.get('error', 'Unknown error')}")
                except:
                    st.error(f"Response: {response.text}")
        
        except requests.exceptions.ConnectionError:
            st.error("❌ Connection failed! Please ensure the Flask API is running on http://localhost:5000")
            st.info("💡 To start the Flask API, run: `python flask_api/app.py`")
        except Exception as e:
            st.error(f"Error: {str(e)}")

elif st.button("Check Plagiarism"):
    st.warning("Please upload both files before checking.")

