import os
import faiss
import pickle
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
INDEX_PATH = "vectorstore/faiss.index"
METADATA_PATH = "vectorstore/metadata.pkl"

os.makedirs("vectorstore", exist_ok=True)

model = SentenceTransformer(EMBEDDING_MODEL_NAME)

'''def chunk_text(docs: List[dict], chunk_size=500, chunk_overlap=50) -> List[Tuple[str, dict]]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = []
    for doc in docs:
        for chunk in splitter.split_text(doc["text"]):
            chunks.append((chunk, {
                "source": doc["filename"],
                "text": chunk  # 🔥 this is the key!
            }))
    return chunks
'''

def chunk_text(docs: List[dict], chunk_size=500, chunk_overlap=50) -> List[Tuple[str, dict]]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = []
    for doc in docs:
        for chunk in splitter.split_text(doc["text"]):
            chunks.append((
                chunk,
                {
                    "source": doc["filename"],
                    "text": chunk  # ✅ This is essential!
                }
            ))
    return chunks


def build_faiss_index(chunks: List[Tuple[str, dict]]):
    texts, metadatas = zip(*chunks)
    embeddings = model.encode(texts, show_progress_bar=True)

    dim = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadatas, f)

    print(f"Saved FAISS index to {INDEX_PATH} with {len(texts)} vectors.")


