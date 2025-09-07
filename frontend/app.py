import streamlit as st
import requests
import os

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(page_title="🧪 Blood Report Analyzer", layout="centered")

st.title("🧪 Blood Test Report Analyzer")
st.write("Upload your blood test report (PDF) and get some *creative* health insights.")

# Query input
query = st.text_area("Enter your query", "Summarise my Blood Test Report")

# File uploader
uploaded_file = st.file_uploader("Upload Blood Report (PDF)", type=["pdf"])

if st.button("Analyze Report"):
    if uploaded_file is None:
        st.error("⚠️ Please upload a PDF file first.")
    else:
        try:
            # Prepare request
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            data = {"query": query}

            with st.spinner("🔍 Analyzing your report..."):
                response = requests.post(API_URL, files=files, data=data)

            if response.status_code == 200:
                result = response.json()
                st.success("✅ Analysis complete!")

                st.subheader("📋 Query")
                st.write(result["query"])

                st.subheader("📑 File Processed")
                st.write(result["file_processed"])

                st.subheader("🧾 Analysis Result")
                st.write(result["analysis"])

                st.subheader("💾 Saved To")
                st.code(result["output_saved_to"])

            else:
                st.error(f" Error: {response.text}")

        except Exception as e:
            st.error(f"⚠️ Failed to connect to API: {str(e)}")
