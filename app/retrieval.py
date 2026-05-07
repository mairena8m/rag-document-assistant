from app.embeddings import embed_query
from app.vector_store import search_chunks
from app.schemas import RetrievalSearchResponse, SourceChunk
from app.retrieval_utils import filter_chunks_by_distance


def search_relevant_chunks(question: str, top_k: int = 4) -> RetrievalSearchResponse:
    query_embedding = embed_query(question)
    retrieved_chunks = search_chunks(query_embedding, top_k=top_k)

    filtered_chunks = filter_chunks_by_distance(retrieved_chunks)

    results = [
        SourceChunk(
            document_name=chunk["document_name"],
            chunk_id=chunk["chunk_id"],
            text=chunk["text"],
            distance=chunk.get("distance")
        )
        for chunk in filtered_chunks
    ]

    return RetrievalSearchResponse(
        query=question,
        results=results
    )