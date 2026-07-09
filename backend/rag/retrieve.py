"""
Loads the pre-built FAISS index and exposes a retrieve() function used by
all specialized agents to pull relevant company-document context.
"""
import os
import pickle
import threading
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VECTORSTORE_DIR = os.path.join(BASE_DIR, "backend", "vectorstore")
EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_lock = threading.Lock()
_model = None
_index = None
_meta = None


def _lazy_load():
    """Load model + index once, on first use, and cache in memory.
    Avoids reloading the embedding model on every request."""
    global _model, _index, _meta
    with _lock:
        if _model is None:
            _model = SentenceTransformer(EMBED_MODEL_NAME)
        if _index is None:
            index_path = os.path.join(VECTORSTORE_DIR, "kb.index")
            meta_path = os.path.join(VECTORSTORE_DIR, "kb_meta.pkl")
            if not os.path.exists(index_path):
                raise FileNotFoundError(
                    "FAISS index not found. Run: python -m backend.rag.ingest"
                )
            _index = faiss.read_index(index_path)
            with open(meta_path, "rb") as f:
                _meta = pickle.load(f)


def retrieve(query: str, top_k: int = 4) -> list[dict]:
    """Returns top_k most relevant knowledge-base chunks for a query,
    each with 'text', 'source', and 'score'."""
    _lazy_load()
    query_vec = _model.encode([query], convert_to_numpy=True).astype("float32")
    faiss.normalize_L2(query_vec)
    scores, indices = _index.search(query_vec, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        chunk = _meta[idx]
        results.append({
            "text": chunk["text"],
            "source": chunk["source"],
            "score": float(score),
        })
    return results


def format_context(chunks: list[dict]) -> str:
    """Formats retrieved chunks into a context block for the LLM prompt."""
    if not chunks:
        return "No relevant company documents found."
    parts = []
    for c in chunks:
        parts.append(f"[Source: {c['source']}]\n{c['text']}")
    return "\n\n".join(parts)


if __name__ == "__main__":
    # quick manual test
    test_query = "How long do I have to return a product?"
    hits = retrieve(test_query)
    for h in hits:
        print(f"({h['score']:.3f}) [{h['source']}] {h['text'][:100]}...")
