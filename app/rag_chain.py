from app.embeddings import embed_query
from app.vector_store import search_chunks
from app.llm_client import generate_answer
from app.schemas import AskResponse, SourceChunk


def ask_question(question: str, top_k: int = 4) -> AskResponse:
    query_embedding = embed_query(question)
    retrieved_chunks = search_chunks(query_embedding, top_k=top_k)

    if not retrieved_chunks:
        return AskResponse(
            answer="No hay documentos cargados o no se ha encontrado contexto relevante.",
            sources=[]
        )

    context_parts = []

    for index, chunk in enumerate(retrieved_chunks, start=1):
        context_parts.append(
            f"[Fuente {index} | Documento: {chunk['document_name']} | Chunk: {chunk['chunk_id']}]\n"
            f"{chunk['text']}"
        )

    context = "\n\n".join(context_parts)
    answer = generate_answer(question, context)

    sources = [
        SourceChunk(
            document_name=chunk["document_name"],
            chunk_id=chunk["chunk_id"],
            text=chunk["text"],
            distance=chunk.get("distance")
        )
        for chunk in retrieved_chunks
    ]

    return AskResponse(answer=answer, sources=sources)