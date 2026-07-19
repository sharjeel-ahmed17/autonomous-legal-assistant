from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from app.database.models.base import BaseModel


class UserRoleLink(SQLModel, table=True):
    __tablename__ = "user_roles"

    user_id: UUID = Field(foreign_key="users.id", primary_key=True)
    role_id: UUID = Field(foreign_key="roles.id", primary_key=True)


class RolePermissionLink(SQLModel, table=True):
    __tablename__ = "role_permissions"

    role_id: UUID = Field(foreign_key="roles.id", primary_key=True)
    permission_id: UUID = Field(foreign_key="permissions.id", primary_key=True)


class Role(BaseModel, table=True):
    __tablename__ = "roles"

    name: str = Field(unique=True, index=True)
    codename: str = Field(unique=True, index=True)
    description: str | None = None
    is_system_role: bool = False
    metadata: str | None = None

    users: list["User"] = Relationship(back_populates="roles", link_model=UserRoleLink)
    permissions: list["Permission"] = Relationship(back_populates="roles", link_model=RolePermissionLink)
