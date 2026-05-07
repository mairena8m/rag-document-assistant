import os
import shutil
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException

from app.schemas import AskRequest, AskResponse, RetrievalSearchRequest, RetrievalSearchResponse
from app.retrieval import search_relevant_chunks
from app.config import UPLOADS_PATH
from app.document_loader import load_document
from app.text_splitter import split_text
from app.embeddings import embed_texts
from app.vector_store import add_chunks, list_documents, reset_collection
from app.rag_chain import ask_question

app = FastAPI(
    title="RAG Document Assistant",
    description="API REST para hacer preguntas sobre documentos usando RAG con Gemini y Chroma.",
    version="0.1.0"
)

Path(UPLOADS_PATH).mkdir(parents=True, exist_ok=True)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        filename = file.filename

        if not filename:
            raise HTTPException(status_code=400, detail="El archivo no tiene nombre.")

        suffix = Path(filename).suffix.lower()

        if suffix not in [".pdf", ".txt"]:
            raise HTTPException(status_code=400, detail="Formato no soportado. Usa PDF o TXT.")

        file_path = os.path.join(UPLOADS_PATH, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = load_document(file_path)
        chunks = split_text(text)

        if not chunks:
            raise HTTPException(status_code=400, detail="No se ha podido extraer texto del documento.")

        embeddings = embed_texts(chunks)
        num_chunks = add_chunks(filename, chunks, embeddings)

        return {
            "document_name": filename,
            "chunks_created": num_chunks,
            "status": "indexed"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando documento: {str(e)}")


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    try:
        return ask_question(
            question=request.question,
            top_k=request.top_k
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando respuesta: {str(e)}")


@app.get("/documents")
def documents():
    return {
        "documents": list_documents()
    }


@app.delete("/documents/reset")
def reset_documents():
    reset_collection()
    return {
        "status": "collection reset"
    }
    
@app.post("/retrieval/search", response_model=RetrievalSearchResponse)
def retrieval_search(request: RetrievalSearchRequest):
    try:
        return search_relevant_chunks(
            question=request.question,
            top_k=request.top_k
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error recuperando chunks relevantes: {str(e)}"
        )