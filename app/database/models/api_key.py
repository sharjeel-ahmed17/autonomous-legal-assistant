from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime
from sqlmodel import Field, Relationship

from app.database.models.base import BaseModel


class ApiKey(BaseModel, table=True):
    __tablename__ = "api_keys"

    user_id: UUID = Field(foreign_key="users.id")
    key_hash: str
    key_prefix: str
    name: str
    scopes: str | None = None

    is_active: bool = True
    last_used_at: datetime | None = Field(sa_type=DateTime(timezone=True))
    expires_at: datetime | None = Field(sa_type=DateTime(timezone=True))

    user: "User" = Relationship(back_populates="api_keys")
