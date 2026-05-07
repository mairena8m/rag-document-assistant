from app.retrieval_utils import filter_chunks_by_distance


def test_filter_chunks_by_distance_keeps_close_chunks():
    chunks = [
        {"chunk_id": "1", "distance": 0.57},
        {"chunk_id": "2", "distance": 0.58},
        {"chunk_id": "3", "distance": 0.61},
    ]

    filtered = filter_chunks_by_distance(chunks, max_distance_margin=0.025)

    assert len(filtered) == 2
    assert filtered[0]["chunk_id"] == "1"
    assert filtered[1]["chunk_id"] == "2"


def test_filter_chunks_by_distance_returns_empty_list_when_no_chunks():
    assert filter_chunks_by_distance([]) == []


def test_filter_chunks_by_distance_returns_original_when_no_distance():
    chunks = [
        {"chunk_id": "1"},
        {"chunk_id": "2"}
    ]

    filtered = filter_chunks_by_distance(chunks)

    assert filtered == chunks