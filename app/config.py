import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_GENERATION_MODEL = os.getenv("GEMINI_GENERATION_MODEL", "gemini-2.5-flash-lite")
GEMINI_EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001")

CHROMA_PATH = os.getenv("CHROMA_PATH", "data/chroma")
UPLOADS_PATH = os.getenv("UPLOADS_PATH", "data/uploads")

if not GEMINI_API_KEY:
    raise RuntimeError("Falta GEMINI_API_KEY en el archivo .env")