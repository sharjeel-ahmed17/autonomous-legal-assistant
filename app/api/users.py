from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.auth import Permission, Role, require_permission, require_role
from app.database.models.user import User
from app.database.schemas.common import PagedResponse
from app.database.schemas.permission import PermissionRead
from app.database.schemas.role import RoleRead
from app.database.schemas.user import UserRead, UserUpdate
from app.dependencies import UserServiceDep

router = APIRouter(prefix="/users", tags=["users"])


class RoleAssignmentRequest(BaseModel):
    role_id: UUID


@router.get("", response_model=PagedResponse)
async def list_users(
    user_service: UserServiceDep,
    page: int = 1,
    page_size: int = 20,
    is_active: bool | None = None,
    is_superuser: bool | None = None,
    _: User = Depends(require_role(Role.ADMIN)),
) -> PagedResponse:
    return await user_service.list_users(
        page=page,
        page_size=page_size,
        is_active=is_active,
        is_superuser=is_superuser,
    )


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_service: UserServiceDep,
    user_id: UUID,
    _: User = Depends(require_permission(Permission.USERS_READ)),
) -> UserRead:
    return await user_service.get_by_id(str(user_id))


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_service: UserServiceDep,
    user_id: UUID,
    payload: UserUpdate,
    _: User = Depends(require_permission(Permission.USERS_UPDATE)),
) -> UserRead:
    return await user_service.update_user(str(user_id), payload)


@router.post("/{user_id}/deactivate", response_model=UserRead)
async def deactivate_user(
    user_service: UserServiceDep,
    user_id: UUID,
    _: User = Depends(require_permission(Permission.USERS_UPDATE)),
) -> UserRead:
    return await user_service.deactivate_user(str(user_id))


@router.post("/{user_id}/activate", response_model=UserRead)
async def activate_user(
    user_service: UserServiceDep,
    user_id: UUID,
    _: User = Depends(require_permission(Permission.USERS_UPDATE)),
) -> UserRead:
    return await user_service.activate_user(str(user_id))


@router.get("/{user_id}/roles", response_model=list[RoleRead])
async def get_user_roles(
    user_service: UserServiceDep,
    user_id: UUID,
    _: User = Depends(require_permission(Permission.USERS_READ)),
) -> list[RoleRead]:
    return await user_service.get_user_roles(str(user_id))


@router.post("/{user_id}/roles", response_model=RoleRead, status_code=201)
async def assign_role(
    user_service: UserServiceDep,
    user_id: UUID,
    payload: RoleAssignmentRequest,
    _: User = Depends(require_role(Role.ADMIN)),
) -> RoleRead:
    return await user_service.assign_role(str(user_id), str(payload.role_id))


@router.delete("/{user_id}/roles/{role_id}", status_code=204)
async def remove_role(
    user_service: UserServiceDep,
    user_id: UUID,
    role_id: UUID,
    _: User = Depends(require_role(Role.ADMIN)),
) -> None:
    await user_service.remove_role(str(user_id), str(role_id))


@router.get("/{user_id}/permissions", response_model=list[PermissionRead])
async def get_user_permissions(
    user_service: UserServiceDep,
    user_id: UUID,
    _: User = Depends(require_permission(Permission.USERS_READ)),
) -> list[PermissionRead]:
    return await user_service.get_user_permissions(str(user_id))
