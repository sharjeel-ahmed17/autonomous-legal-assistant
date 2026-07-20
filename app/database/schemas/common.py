from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=20, ge=1, le=100, description="Items per page")


class PagedResponse(BaseModel):
    items: list
    total: int
    page: int
    page_size: int
    total_pages: int


class SuccessResponse(BaseModel):
    message: str = "Success"
    data: dict | None = None


class ErrorResponse(BaseModel):
    detail: str
    error_code: str | None = None
    errors: list[dict] | None = None


class MessageResponse(BaseModel):
    message: str


class UUIDBaseSchema(BaseModel):
    id: UUID


class TimestampSchema(BaseModel):
    created_at: datetime
    updated_at: datetime


class AuditSchema(BaseModel):
    created_at: datetime
    updated_at: datetime
