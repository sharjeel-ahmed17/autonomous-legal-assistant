from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.database.schemas.common import TimestampSchema, UUIDBaseSchema


class RefreshTokenCreate(BaseModel):
    user_id: UUID
    token_hash: str
    expires_at: datetime
    device_info: str | None = None
    ip_address: str | None = None


class RefreshTokenRead(UUIDBaseSchema, TimestampSchema):
    user_id: UUID
    expires_at: datetime
    is_revoked: bool
    device_info: str | None
    ip_address: str | None
