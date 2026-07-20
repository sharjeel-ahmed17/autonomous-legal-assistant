from uuid import UUID

from pydantic import BaseModel

from app.database.schemas.common import TimestampSchema, UUIDBaseSchema


class NotificationCreate(BaseModel):
    title: str
    body: str
    type: str = "info"
    metadata_json: str | None = None


class NotificationUpdate(BaseModel):
    is_read: bool = True


class NotificationRead(UUIDBaseSchema, TimestampSchema):
    user_id: UUID
    title: str
    body: str
    type: str
    is_read: bool
    metadata_json: str | None
