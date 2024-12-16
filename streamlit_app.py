import streamlit as st
import requests

# FastAPI endpoints
UPLOAD_URL = "http://localhost:8000/upload_document"
QUERY_URL = "http://localhost:8000/ask_question"

st.title("Contextual Document Chatbot")

# File upload section
st.header("Upload a Document")
uploaded_file = st.file_uploader("Choose a file (PDF or Word)", type=["pdf", "docx"])
if uploaded_file is not None:
    files = {"file": uploaded_file.getvalue()}
    response = requests.post(UPLOAD_URL, files={"file": uploaded_file})
    if response.status_code == 200:
        st.success("Document uploaded and processed successfully!")
    else:
        st.error("Error uploading the document.")

# Query section
st.header("Ask a Question")
question = st.text_input("Enter your question:")
if st.button("Submit Question"):
    response = requests.post(QUERY_URL, json={"query": question})
    if response.status_code == 200:
        st.write("**Answer:**", response.json().get("answer", "No answer found."))
    else:
        st.error("Error fetching the answer.")
