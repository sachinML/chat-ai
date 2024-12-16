from typing import List
import numpy as np
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection

# Milvus connection
# Adjust host and port as needed if not local
connections.connect("default", host="localhost", port="19530")

COLLECTION_NAME = "documents_collection"

# Define the schema
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
]

schema = CollectionSchema(
    fields=fields, description="A collection of document embeddings"
)

# Create or load the collection
collection = Collection(name=COLLECTION_NAME, schema=schema)

# Create an index on the embedding field
if not collection.has_index():
    index_params = {
        "metric_type": "IP",  # inner product or cosine similarity
        "index_type": "IVF_FLAT",
        "params": {"nlist": 1024},
    }
    collection.create_index(field_name="embedding", index_params=index_params)

collection.load()


class MilvusVectorStore:
    def __init__(self):
        self.collection = collection

    def add_documents(self, embeddings: np.ndarray, texts: List[str]):
        # Insert data into the collection
        entities = [embeddings.tolist(), texts]
        self.collection.insert([entities[0], entities[1]])
        self.collection.flush()

    def similarity_search(
        self, query_embedding: np.ndarray, top_k: int = 3
    ) -> List[str]:
        search_params = {"metric_type": "IP", "params": {"nprobe": 10}}
        query_embedding = [query_embedding.tolist()]
        results = self.collection.search(
            data=query_embedding,
            anns_field="embedding",
            param=search_params,
            limit=top_k,
            output_fields=["text"],
        )
        # results is a list of queries
        hits = results[0]
        return [hit.entity.get("text") for hit in hits]
