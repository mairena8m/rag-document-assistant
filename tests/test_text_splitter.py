import pytest

from app.text_splitter import split_text


def test_split_text_returns_chunks():
    text = "a" * 2000

    chunks = split_text(text, chunk_size=500, overlap=100)

    assert len(chunks) > 1
    assert all(len(chunk) <= 500 for chunk in chunks)


def test_split_text_returns_empty_list_for_empty_text():
    chunks = split_text("   ")

    assert chunks == []


def test_split_text_raises_error_when_overlap_is_greater_than_chunk_size():
    with pytest.raises(ValueError, match="overlap debe ser menor"):
        split_text("texto de prueba", chunk_size=100, overlap=100)


def test_split_text_raises_error_when_chunk_size_is_invalid():
    with pytest.raises(ValueError, match="chunk_size debe ser mayor"):
        split_text("texto de prueba", chunk_size=0, overlap=10)
        
def test_split_text_filters_low_quality_chunks():
    text = "Índice de Figuras . . . . . . . . . . . . . . . . . . . ."

    chunks = split_text(text, chunk_size=200, overlap=50)

    assert chunks == []