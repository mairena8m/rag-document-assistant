import uuid
import chromadb

from app.config import CHROMA_PATH

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name="documents")


def add_chunks(document_name: str, chunks: list[str], embeddings: list[list[float]]) -> int:
    ids = []
    metadatas = []

    for index, _ in enumerate(chunks):
        chunk_id = f"{document_name}_{index}_{uuid.uuid4().hex[:8]}"
        ids.append(chunk_id)
        metadatas.append({
            "document_name": document_name,
            "chunk_index": index
        })

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(chunks)


def search_chunks(query_embedding: list[float], top_k: int = 4) -> list[dict]:
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    ids = results.get("ids", [[]])[0]

    retrieved = []

    for chunk_id, text, metadata in zip(ids, documents, metadatas):
        retrieved.append({
            "chunk_id": chunk_id,
            "text": text,
            "document_name": metadata.get("document_name", "unknown")
        })

    return retrieved


def list_documents() -> list[str]:
    data = collection.get(include=["metadatas"])

    documents = set()

    for metadata in data.get("metadatas", []):
        documents.add(metadata.get("document_name", "unknown"))

    return sorted(documents)


def reset_collection() -> None:
    global collection

    client.delete_collection(name="documents")
    collection = client.get_or_create_collection(name="documents")