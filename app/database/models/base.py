
from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel


class TimestampMixin(SQLModel):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_type=DateTime(timezone=True),
        nullable=False,
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_type=DateTime(timezone=True),
        nullable=False,
        sa_column_kwargs={
            "onupdate": lambda: datetime.now(UTC),
        },
    )


class UUIDMixin(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)


class BaseModel(UUIDMixin, TimestampMixin):
    pass

