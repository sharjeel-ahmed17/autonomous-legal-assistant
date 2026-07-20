from typing import Optional
from uuid import UUID

from sqlmodel import Field, Relationship

from app.database.models.base import BaseModel


class Citation(BaseModel, table=True):
    __tablename__ = "citations"

    document_id: UUID = Field(foreign_key="documents.id")
    message_id: UUID | None = Field(default=None, foreign_key="messages.id")
    agent_run_id: UUID | None = Field(default=None, foreign_key="agent_runs.id")

    citation_text: str
    source_page: int | None = None
    relevance_score: float | None = None
    metadata_json: str | None = None

    document: "Document" = Relationship(back_populates="citations")
    message: Optional["Message"] = Relationship(back_populates="citations")
    agent_run: Optional["AgentRun"] = Relationship(back_populates="citations")
