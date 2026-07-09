"""
Ingests all PDFs from knowledge_base/, chunks them, embeds them with
sentence-transformers, and builds a local FAISS index.

Run: python -m backend.rag.ingest   (from project root)
"""
import os
import pickle
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KB_DIR = os.path.join(BASE_DIR, "knowledge_base")
VECTORSTORE_DIR = os.path.join(BASE_DIR, "backend", "vectorstore")
EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

CHUNK_SIZE = 400        # characters per chunk
CHUNK_OVERLAP = 60      # overlap between consecutive chunks


def load_pdf_text(path: str) -> str:
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def chunk_text(text: str, source: str) -> list[dict]:
    """Simple sliding-window character chunker. Keeps things dependency-light
    (no LangChain splitter needed) while still giving overlap for context continuity."""
    text = " ".join(text.split())  # normalize whitespace
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end]
        if chunk.strip():
            chunks.append({"text": chunk, "source": source})
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


def build_index():
    if not os.path.isdir(KB_DIR):
        raise FileNotFoundError(f"Knowledge base directory not found: {KB_DIR}")

    pdf_files = [f for f in os.listdir(KB_DIR) if f.lower().endswith(".pdf")]
    if not pdf_files:
        raise FileNotFoundError(f"No PDFs found in {KB_DIR}. Run generate_kb.py first.")

    all_chunks = []
    for fname in sorted(pdf_files):
        path = os.path.join(KB_DIR, fname)
        text = load_pdf_text(path)
        chunks = chunk_text(text, source=fname)
        all_chunks.extend(chunks)
        print(f"  {fname}: {len(chunks)} chunks")

    print(f"\nTotal chunks: {len(all_chunks)}")
    print(f"Loading embedding model: {EMBED_MODEL_NAME} (first run downloads ~90MB)")
    model = SentenceTransformer(EMBED_MODEL_NAME)

    texts = [c["text"] for c in all_chunks]
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    embeddings = embeddings.astype("float32")

    # Normalize for cosine similarity via inner product
    faiss.normalize_L2(embeddings)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    faiss.write_index(index, os.path.join(VECTORSTORE_DIR, "kb.index"))
    with open(os.path.join(VECTORSTORE_DIR, "kb_meta.pkl"), "wb") as f:
        pickle.dump(all_chunks, f)

    print(f"\nSaved FAISS index + metadata to {VECTORSTORE_DIR}")
    return index, all_chunks


if __name__ == "__main__":
    build_index()
