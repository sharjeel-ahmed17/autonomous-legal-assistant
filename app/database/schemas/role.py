from uuid import UUID

from pydantic import BaseModel, Field

from app.database.schemas.common import TimestampSchema, UUIDBaseSchema


class RoleCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    codename: str = Field(min_length=1, max_length=100)
    description: str | None = None
    is_system_role: bool = False
    metadata_json: str | None = None


class RoleUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    metadata_json: str | None = None


class RoleRead(UUIDBaseSchema, TimestampSchema):
    name: str
    codename: str
    description: str | None
    is_system_role: bool
    metadata_json: str | None
