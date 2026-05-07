from google import genai
from google.genai import types

from app.config import GEMINI_API_KEY, GEMINI_GENERATION_MODEL

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_answer(question: str, context: str) -> str:
    prompt = f"""
Responde a la pregunta usando únicamente el contexto proporcionado.

Reglas:
- Si el contexto no contiene información suficiente, dilo claramente.
- No inventes datos.
- No uses conocimiento externo.
- Responde de forma clara, técnica y breve.
- Si hay incertidumbre, explícala.

Contexto:
{context}

Pregunta:
{question}
"""

    response = client.models.generate_content(
        model=GEMINI_GENERATION_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2
        )
    )

    return response.text