from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3)
    top_k: int = Field(default=4, ge=1, le=10)


class SourceChunk(BaseModel):
    document_name: str
    chunk_id: str
    text: str


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]