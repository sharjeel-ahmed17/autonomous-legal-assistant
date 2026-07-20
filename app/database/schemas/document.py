from uuid import UUID

from pydantic import BaseModel, Field

from app.database.schemas.common import TimestampSchema, UUIDBaseSchema


class DocumentCreate(BaseModel):
    filename: str
    file_path: str
    file_size: int
    mime_type: str
    page_count: int | None = None


class DocumentUpdate(BaseModel):
    filename: str | None = None
    file_path: str | None = None
    status: str | None = None
    page_count: int | None = None


class DocumentRead(UUIDBaseSchema, TimestampSchema):
    filename: str
    file_path: str
    file_size: int
    mime_type: str
    status: str
    page_count: int | None
    owner_id: UUID
