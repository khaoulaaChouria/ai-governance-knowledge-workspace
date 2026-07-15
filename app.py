import streamlit as st
from services.pdf_reader import extract_text

st.set_page_config(
    page_title="AI Governance Knowledge Workspace",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI Governance Knowledge Workspace")

st.write(
    "Upload business documents to build your organization's governance knowledge base."
)

uploaded_file = st.file_uploader(
    "Choose a PDF document",
    type=["pdf"]
)

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")

    text = extract_text(uploaded_file)

    st.subheader("Extracted Text")

    st.write(text)