# main.py
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from utils.doc_parser import parse_document
from utils.embeddings import get_embeddings_for_chunks, get_embedding
from utils.vector_store import MilvusVectorStore
from utils.llm import generate_answer

app = FastAPI()

# Initialize the Milvus vector store
vector_store = MilvusVectorStore()


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


class QueryRequest(BaseModel):
    query: str


@app.post("/upload_document")
async def upload_document(file: UploadFile = File(...)):
    file_bytes = await file.read()
    text = parse_document(file_bytes, file.filename)
    document_chunks = chunk_text(text)

    embeddings = get_embeddings_for_chunks(document_chunks)
    vector_store.add_documents(embeddings, document_chunks)

    return {"status": "success", "chunks_added": len(document_chunks)}


@app.post("/ask_question")
async def ask_question(payload: QueryRequest):
    query = payload.query
    query_emb = get_embedding(query)
    top_chunks = vector_store.similarity_search(query_emb, top_k=3)
    context = "\n".join(top_chunks)
    answer = generate_answer(context, query)
    if "I don't know the answer" in answer:
        return {"answer": "I don't know the answer"}
    return {"answer": answer}


@app.get("/health")
def health_check():
    return {"status": "ok"}
