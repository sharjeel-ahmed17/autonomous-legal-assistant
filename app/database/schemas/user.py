from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.database.schemas.common import TimestampSchema, UUIDBaseSchema


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)
    full_name: str | None = None


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = Field(default=None, min_length=3, max_length=50)
    full_name: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None


class UserRead(UUIDBaseSchema, TimestampSchema):
    email: str
    username: str
    full_name: str | None
    is_active: bool
    is_superuser: bool
