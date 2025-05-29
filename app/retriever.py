'''import faiss
import pickle
from sentence_transformers import SentenceTransformer
from typing import List

INDEX_PATH = "vectorstore/faiss.index"
METADATA_PATH = "vectorstore/metadata.pkl"
model = SentenceTransformer("all-MiniLM-L6-v2")

def load_faiss_index():
    index = faiss.read_index(INDEX_PATH)
    with open(METADATA_PATH, "rb") as f:
        metadatas = pickle.load(f)
    return index, metadatas

def search(query: str, k=5) -> List[dict]:
    index, metadatas = load_faiss_index()
    q_vec = model.encode([query])
    D, I = index.search(q_vec, k)
    print(f"Top result metadata: {metadatas[I[0][0]]}")


    results = []
    for i in I[0]:
        if i < len(metadatas):
            results.append(metadatas[i])
    return results
'''

import faiss
import pickle
from sentence_transformers import SentenceTransformer
from typing import List, Dict

INDEX_PATH = "vectorstore/faiss.index"
METADATA_PATH = "vectorstore/metadata.pkl"
model = SentenceTransformer("all-MiniLM-L6-v2")

def load_faiss_index():
    index = faiss.read_index(INDEX_PATH)
    with open(METADATA_PATH, "rb") as f:
        metadatas = pickle.load(f)
    return index, metadatas

def search(query: str, k=5) -> List[Dict]:
    index, metadatas = load_faiss_index()
    query_vector = model.encode([query])
    _, I = index.search(query_vector, k)

    results = []
    for i in I[0]:
        if i < len(metadatas):
            results.append(metadatas[i])
    return results
