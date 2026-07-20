from __future__ import annotations

from sqlmodel import Field

from app.database.models.base import BaseModel


class Workflow(BaseModel, table=True):
    __tablename__ = "workflows"

    name: str = Field(unique=True, index=True)
    description: str | None = None
    version: str = "1.0.0"
    config: str | None = None
    is_active: bool = True
    metadata_json: str | None = None
