import re
import time

from google import genai
from google.genai import types

from app.config import GEMINI_API_KEY, GEMINI_EMBEDDING_MODEL

client = genai.Client(api_key=GEMINI_API_KEY)


def _is_rate_limit_error(error: Exception) -> bool:
    error_text = str(error).lower()
    return (
        "429" in error_text
        or "resource_exhausted" in error_text
        or "quota" in error_text
        or "rate" in error_text
    )


def _extract_retry_seconds(error: Exception, default_seconds: int = 35) -> int:
    error_text = str(error)

    match = re.search(r"retryDelay': '(\d+)s", error_text)
    if match:
        return int(match.group(1)) + 2

    match = re.search(r"retry in ([\d.]+)s", error_text, re.IGNORECASE)
    if match:
        return int(float(match.group(1))) + 2

    return default_seconds


def embed_text(text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> list[float]:
    response = client.models.embed_content(
        model=GEMINI_EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            task_type=task_type
        )
    )

    return response.embeddings[0].values


def embed_text_with_retry(
    text: str,
    task_type: str = "RETRIEVAL_DOCUMENT",
    max_retries: int = 3
) -> list[float]:
    for attempt in range(max_retries):
        try:
            return embed_text(text=text, task_type=task_type)

        except Exception as e:
            if _is_rate_limit_error(e) and attempt < max_retries - 1:
                wait_seconds = _extract_retry_seconds(e)
                print(f"Rate limit alcanzado. Esperando {wait_seconds} segundos...")
                time.sleep(wait_seconds)
                continue

            raise


def embed_texts(
    texts: list[str],
    task_type: str = "RETRIEVAL_DOCUMENT",
    delay_seconds: float = 0.8
) -> list[list[float]]:
    embeddings = []

    total = len(texts)

    for index, text in enumerate(texts, start=1):
        print(f"Generando embedding {index}/{total}")

        embedding = embed_text_with_retry(
            text=text,
            task_type=task_type
        )

        embeddings.append(embedding)

        if index < total:
            time.sleep(delay_seconds)

    return embeddings


def embed_query(question: str) -> list[float]:
    return embed_text_with_retry(
        text=question,
        task_type="RETRIEVAL_QUERY"
    )