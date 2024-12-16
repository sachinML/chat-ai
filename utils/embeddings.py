from sentence_transformers import SentenceTransformer
import numpy as np

# Load a sentence-transformer model for embeddings
# You can choose any model from HuggingFace that fits your environment.
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)


def get_embedding(text: str) -> np.ndarray:
    return embedding_model.encode([text])[0]


def get_embeddings_for_chunks(chunks: list) -> np.ndarray:
    return embedding_model.encode(chunks)
