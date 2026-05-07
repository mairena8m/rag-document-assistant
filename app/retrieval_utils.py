def filter_chunks_by_distance(
    chunks: list[dict],
    max_distance_margin: float = 0.025
) -> list[dict]:
    if not chunks:
        return []

    best_distance = chunks[0].get("distance")

    if best_distance is None:
        return chunks

    max_allowed_distance = best_distance + max_distance_margin

    filtered_chunks = [
        chunk for chunk in chunks
        if chunk.get("distance") is not None
        and chunk["distance"] <= max_allowed_distance
    ]

    return filtered_chunks