import chromadb
from pypdf import PdfReader
import os

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("docs")

def chunk_text(text, size=800, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start+size])
        start += size - overlap
    return chunks

def ingest_pdf(filepath):
    reader = PdfReader(filepath)
    full_text = "\n".join(page.extract_text() or "" for page in reader.pages)
    chunks = chunk_text(full_text)
    ids = [f"{os.path.basename(filepath)}_{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, ids=ids,
                    metadatas=[{"source": filepath}] * len(chunks))
    print(f"Ingested {len(chunks)} chunks from {filepath}")

if __name__ == "__main__":
    for f in os.listdir("./docs"):
        if f.endswith(".pdf"):
            ingest_pdf(f"./docs/{f}")
