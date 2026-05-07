def split_text(text: str, chunk_size: int = 1600, overlap: int = 200) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size debe ser mayor que 0")

    if overlap >= chunk_size:
        raise ValueError("overlap debe ser menor que chunk_size")

    clean_text = " ".join(text.split())

    if not clean_text:
        return []

    chunks = []
    start = 0

    while start < len(clean_text):
        end = start + chunk_size
        chunk = clean_text[start:end]

        if chunk.strip() and not is_low_quality_chunk(chunk):
            chunks.append(chunk.strip())

        start += chunk_size - overlap

    return chunks

def is_low_quality_chunk(chunk: str) -> bool:
    lowered = chunk.lower()

    bad_patterns = [
        "índice de figuras",
        "índice de tablas",
        "referencias",
        ". . . . .",
        "lista de figuras",
        "lista de tablas",
        "agradecimientos",
        "no puedo finalizar sin mencionar",
        "huelva, 2025"
    ]

    if any(pattern in lowered for pattern in bad_patterns):
        return True

    if len(chunk.strip()) < 80:
        return True

    return False
