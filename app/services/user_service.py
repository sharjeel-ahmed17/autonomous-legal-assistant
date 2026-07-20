from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.exceptions import (
    ConflictException,
    NotFoundException,
)
from app.core.security import hash_password, verify_password
from app.database.models.permission import Permission
from app.database.models.role import UserRoleLink
from app.database.models.user import User
from app.database.repositories.permission import PermissionRepository
from app.database.repositories.role import RoleRepository
from app.database.repositories.user import UserRepository
from app.database.schemas.common import PagedResponse
from app.database.schemas.permission import PermissionRead
from app.database.schemas.role import RoleRead
from app.database.schemas.user import UserRead, UserUpdate


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository()
        self.role_repo = RoleRepository()
        self.permission_repo = PermissionRepository()

    async def get_by_id(self, user_id: str | UUID) -> UserRead:
        user = await self.user_repo.get_by_id(self.session, user_id)
        if not user:
            raise NotFoundException("User not found.")
        return self._to_read(user)

    async def get_by_email(self, email: str) -> UserRead:
        user = await self.user_repo.get_by_email(self.session, email)
        if not user:
            raise NotFoundException("User not found.")
        return self._to_read(user)

    async def update_user(self, user_id: str | UUID, payload: UserUpdate) -> UserRead:
        user = await self.user_repo.get_by_id(self.session, user_id)
        if not user:
            raise NotFoundException("User not found.")

        update_data = payload.model_dump(exclude_unset=True)

        if "email" in update_data and update_data["email"] != user.email:
            exists = await self.user_repo.email_exists(
                self.session, update_data["email"]
            )
            if exists:
                raise ConflictException("Email is already in use.")

        for field, value in update_data.items():
            setattr(user, field, value)

        user = await self.user_repo.update(self.session, user)
        return self._to_read(user)

    async def deactivate_user(self, user_id: str | UUID) -> UserRead:
        user = await self.user_repo.get_by_id(self.session, user_id)
        if not user:
            raise NotFoundException("User not found.")
        user.is_active = False
        user = await self.user_repo.update(self.session, user)
        return self._to_read(user)

    async def activate_user(self, user_id: str | UUID) -> UserRead:
        user = await self.user_repo.get_by_id(self.session, user_id)
        if not user:
            raise NotFoundException("User not found.")
        user.is_active = True
        user = await self.user_repo.update(self.session, user)
        return self._to_read(user)

    async def list_users(
        self,
        page: int = 1,
        page_size: int = 20,
        is_active: bool | None = None,
        is_superuser: bool | None = None,
    ) -> PagedResponse:
        statement = select(User).offset((page - 1) * page_size).limit(page_size)

        if is_active is not None:
            statement = statement.where(User.is_active == is_active)
        if is_superuser is not None:
            statement = statement.where(User.is_superuser == is_superuser)

        result = await self.session.exec(statement)
        users = result.all()

        count_statement = select(User)
        if is_active is not None:
            count_statement = count_statement.where(User.is_active == is_active)
        if is_superuser is not None:
            count_statement = count_statement.where(
                User.is_superuser == is_superuser
            )
        count_result = await self.session.exec(count_statement)
        total = len(count_result.all())

        return PagedResponse(
            items=[self._to_read(u) for u in users],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=max(1, (total + page_size - 1) // page_size),
        )

    async def assign_role(self, user_id: str | UUID, role_id: str | UUID) -> RoleRead:
        user = await self.user_repo.get_by_id(self.session, user_id)
        if not user:
            raise NotFoundException("User not found.")

        role = await self.role_repo.get_by_id(self.session, role_id)
        if not role:
            raise NotFoundException("Role not found.")

        existing_link = await self.session.exec(
            select(UserRoleLink).where(
                UserRoleLink.user_id == user.id,
                UserRoleLink.role_id == role.id,
            )
        )
        if existing_link.first():
            raise ConflictException("User already has this role assigned.")

        link = UserRoleLink(user_id=user.id, role_id=role.id)
        self.session.add(link)
        await self.session.commit()

        return RoleRead(
            id=role.id,
            name=role.name,
            codename=role.codename,
            description=role.description,
            is_system_role=role.is_system_role,
            metadata_json=role.metadata_json,
            created_at=role.created_at,
            updated_at=role.updated_at,
        )

    async def remove_role(self, user_id: str | UUID, role_id: str | UUID) -> None:
        link = await self.session.exec(
            select(UserRoleLink).where(
                UserRoleLink.user_id == user_id,
                UserRoleLink.role_id == role_id,
            )
        )
        link_obj = link.first()
        if not link_obj:
            raise NotFoundException("Role assignment not found.")
        await self.session.delete(link_obj)
        await self.session.commit()

    async def get_user_roles(self, user_id: str | UUID) -> list[RoleRead]:
        user = await self.user_repo.get_by_id(self.session, user_id)
        if not user:
            raise NotFoundException("User not found.")

        await self.session.refresh(user)
        return [
            RoleRead(
                id=r.id,
                name=r.name,
                codename=r.codename,
                description=r.description,
                is_system_role=r.is_system_role,
                metadata_json=r.metadata_json,
                created_at=r.created_at,
                updated_at=r.updated_at,
            )
            for r in user.roles
        ]

    async def get_user_permissions(self, user_id: str | UUID) -> list[PermissionRead]:
        user = await self.user_repo.get_by_id(self.session, user_id)
        if not user:
            raise NotFoundException("User not found.")

        await self.session.refresh(user)

        permission_map: dict[str, Permission] = {}
        for role in user.roles:
            await self.session.refresh(role)
            for perm in role.permissions:
                permission_map[perm.codename] = perm

        return [
            PermissionRead(
                id=p.id,
                name=p.name,
                codename=p.codename,
                description=p.description,
                resource_type=p.resource_type,
                metadata_json=p.metadata_json,
                created_at=p.created_at,
                updated_at=p.updated_at,
            )
            for p in permission_map.values()
        ]

    async def change_password(
        self, user_id: str | UUID, current_password: str, new_password: str
    ) -> None:
        user = await self.user_repo.get_by_id(self.session, user_id)
        if not user:
            raise NotFoundException("User not found.")
        if not verify_password(current_password, user.hashed_password):
            raise ConflictException("Current password is incorrect.")
        user.hashed_password = hash_password(new_password)
        await self.user_repo.update(self.session, user)

    @staticmethod
    def _to_read(user: User) -> UserRead:
        return UserRead(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
