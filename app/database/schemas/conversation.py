from uuid import UUID

from pydantic import BaseModel

from app.database.schemas.common import TimestampSchema, UUIDBaseSchema


class ConversationCreate(BaseModel):
    title: str
    metadata_json: str | None = None


class ConversationUpdate(BaseModel):
    title: str | None = None
    status: str | None = None
    metadata_json: str | None = None


class ConversationRead(UUIDBaseSchema, TimestampSchema):
    title: str
    status: str
    metadata_json: str | None
    user_id: UUID
