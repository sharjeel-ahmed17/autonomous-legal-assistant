from uuid import UUID

from sqlmodel import Field, Relationship

from app.database.models.base import BaseModel


class Document(BaseModel, table=True):
    __tablename__ = "documents"

    filename: str
    file_path: str

    file_size: int

    mime_type: str

    status: str = "uploaded"

    page_count: int | None = None

    owner_id: UUID = Field(foreign_key="users.id")

    owner: "User" = Relationship(back_populates="documents")
    chunks: list["DocumentChunk"] = Relationship(back_populates="document")
