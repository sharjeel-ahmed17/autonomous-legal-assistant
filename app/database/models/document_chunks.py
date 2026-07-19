from uuid import UUID

from sqlmodel import Field, Relationship

from app.database.models.base import BaseModel


class DocumentChunk(BaseModel, table=True):
    __tablename__ = "document_chunks"

    document_id: UUID = Field(foreign_key="documents.id")
    chunk_index: int
    content: str
    page_number: int | None = None
    token_count: int | None = None
    metadata: str | None = None
    embedding_id: str | None = None

    document: "Document" = Relationship(back_populates="chunks")
    embeddings: list["Embedding"] = Relationship(back_populates="chunk")
