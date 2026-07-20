from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime
from sqlmodel import Field, Relationship

from app.database.models.base import BaseModel


class RefreshToken(BaseModel, table=True):
    __tablename__ = "refresh_tokens"

    user_id: UUID = Field(foreign_key="users.id")
    token_hash: str
    expires_at: datetime = Field(sa_type=DateTime(timezone=True))
    is_revoked: bool = False
    device_info: str | None = None
    ip_address: str | None = None

    user: "User" = Relationship(back_populates="refresh_tokens")
