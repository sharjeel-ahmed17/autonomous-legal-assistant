from pydantic import BaseModel, Field

from app.database.schemas.common import TimestampSchema, UUIDBaseSchema


class PermissionCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    codename: str = Field(min_length=1, max_length=100)
    description: str | None = None
    resource_type: str | None = None
    metadata_json: str | None = None


class PermissionUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    resource_type: str | None = None
    metadata_json: str | None = None


class PermissionRead(UUIDBaseSchema, TimestampSchema):
    name: str
    codename: str
    description: str | None
    resource_type: str | None
    metadata_json: str | None
