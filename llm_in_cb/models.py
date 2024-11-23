from pydantic import BaseModel


class TextRequest(BaseModel):
    text: str


class EmbeddingResponse(BaseModel):
    embeddings: list[float]
