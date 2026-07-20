from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.database.schemas.common import TimestampSchema, UUIDBaseSchema


class ApiKeyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    scopes: str | None = None
    expires_at: datetime | None = None


class ApiKeyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    scopes: str | None = None
    is_active: bool | None = None


class ApiKeyRead(UUIDBaseSchema, TimestampSchema):
    user_id: UUID
    key_prefix: str
    name: str
    scopes: str | None
    is_active: bool
    last_used_at: datetime | None
    expires_at: datetime | None


class ApiKeyCreated(ApiKeyRead):
    raw_key: str
