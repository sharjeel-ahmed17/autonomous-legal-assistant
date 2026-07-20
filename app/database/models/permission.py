from uuid import UUID

from sqlmodel import Field, Relationship

from app.database.models.base import BaseModel
from app.database.models.role import RolePermissionLink


class Permission(BaseModel, table=True):
    __tablename__ = "permissions"

    name: str = Field(unique=True, index=True)
    codename: str = Field(unique=True, index=True)
    description: str | None = None
    resource_type: str | None = None
    metadata_json: str | None = None

    roles: list["Role"] = Relationship(back_populates="permissions", link_model=RolePermissionLink)
