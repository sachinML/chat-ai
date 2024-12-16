# Contextual Chatbot for Document Querying

## Description
This project is a Contextual Chatbot that can:
1. Accept PDF or Word documents.
2. Answer questions based on the content of the uploaded documents.
3. Use gpt and a vector database for semantic search.

It consists of:
- **FastAPI**: Backend for document upload, chunking, embedding, and querying.
- **Streamlit**: A simple user interface for document upload and querying.
- **Milvus**: A vector database for storing embeddings and performing semantic search.

---

## Features
- **Document Upload**: Upload PDF or Word files.
- **Chunking and Embedding**: Split documents into smaller chunks and generate embeddings.
- **Semantic Search**: Retrieve top chunks based on semantic similarity.
- **Querying**: Answer user questions using context retrieved from embeddings.
- **Simple Interface**: Use a Streamlit-based frontend for interaction.

---

## Setup Instructions

### 1. Run the System with Docker Compose
To build and start all services (FastAPI, Streamlit, Milvus):
docker-compose up --build

### 4. Access the Applications
Once the containers are up and running:

FastAPI Swagger UI:
Access FastAPI for document upload and querying:
http://localhost:8000/docs

Streamlit Frontend:
Upload documents and ask questions:
http://localhost:8501


## How to Use

### 1. Upload a Document
Use the Streamlit interface to upload a document or send a POST request:

curl -X POST "http://localhost:8000/upload_document" \
     -F "file=@/path/to/your/document.pdf"

### 2. Ask a Question
Send a question about the uploaded document:

curl -X POST "http://localhost:8000/ask_question" \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the document about?"}'

