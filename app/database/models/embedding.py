from __future__ import annotations

from uuid import UUID

from sqlmodel import Field, Relationship

from app.database.models.base import BaseModel


class Embedding(BaseModel, table=True):
    __tablename__ = "embeddings"

    document_chunk_id: UUID = Field(foreign_key="document_chunks.id")
    model_name: str
    vector_store_id: str
    dimensions: int
    metadata_json: str | None = None

    chunk: "DocumentChunk" = Relationship(back_populates="embeddings")
