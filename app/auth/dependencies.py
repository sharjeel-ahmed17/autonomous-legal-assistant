"""FastAPI authorization dependencies for RBAC and permission checking.

This module provides dependency factories for role and permission checks,
reusing the existing authentication `_get_current_user` dependency without
decoding JWTs manually or performing duplicate database queries.
"""

from collections.abc import Awaitable, Callable
from typing import Annotated

from fastapi import Depends

from app.auth.exceptions import PermissionDeniedException, RoleDeniedException
from app.auth.permissions import ROLE_PERMISSIONS, Permission
from app.auth.roles import Role
from app.database.models.user import User
from app.dependencies import _get_current_user


def get_user_roles(user: User) -> set[Role]:
    """Extract and normalize all assigned roles from a User instance.

    Args:
        user: The authenticated User object.

    Returns:
        set[Role]: Normalized set of Role enums associated with the user.
    """
    roles: set[Role] = set()

    # Superuser bypass / implicit SUPER_ADMIN role
    if getattr(user, "is_superuser", False):
        roles.add(Role.SUPER_ADMIN)

    # Check user.roles (SQLModel relationship or list of role models/strings)
    user_roles = getattr(user, "roles", None)
    if user_roles:
        for r in user_roles:
            role_val = (
                getattr(r, "codename", None)
                or getattr(r, "name", None)
                or str(r)
            )
            try:
                roles.add(Role(role_val.lower()))
            except ValueError:
                # Handle cases where value might match enum value case-insensitively
                for role_enum in Role:
                    if role_enum.value.lower() == str(role_val).lower():
                        roles.add(role_enum)

    # Check user.role singular attribute if present
    singular_role = getattr(user, "role", None)
    if singular_role:
        role_val = (
            getattr(singular_role, "codename", None)
            or getattr(singular_role, "name", None)
            or str(singular_role)
        )
        try:
            roles.add(Role(role_val.lower()))
        except ValueError:
            pass

    return roles


def get_user_permissions(user: User) -> set[Permission]:
    """Compute the combined set of permissions granted to a User.

    Args:
        user: The authenticated User object.

    Returns:
        set[Permission]: Complete set of granted Permission enums.
    """
    user_roles = get_user_roles(user)
    if Role.SUPER_ADMIN in user_roles or getattr(user, "is_superuser", False):
        return set(Permission)

    permissions: set[Permission] = set()
    for role in user_roles:
        permissions.update(ROLE_PERMISSIONS.get(role, set()))

    return permissions


def require_role(
    required_role: Role | str,
) -> Callable[[User], Awaitable[User]]:
    """Factory producing a FastAPI dependency that enforces a required role.

    Args:
        required_role: The role required to access the route.

    Returns:
        Callable: Dependency returning current user if authorized.
    """
    target_role = (
        Role(required_role)
        if isinstance(required_role, str)
        else required_role
    )

    async def dependency(
        current_user: Annotated[User, Depends(_get_current_user)],
    ) -> User:
        user_roles = get_user_roles(current_user)
        if Role.SUPER_ADMIN in user_roles or target_role in user_roles:
            return current_user
        raise RoleDeniedException(role=target_role)

    return dependency


def require_any_role(
    *required_roles: Role | str,
) -> Callable[[User], Awaitable[User]]:
    """Factory producing a FastAPI dependency enforcing any of the specified roles.

    Args:
        *required_roles: Roles allowed to access the route.

    Returns:
        Callable: Dependency returning current user if authorized.
    """
    target_roles = {
        Role(r) if isinstance(r, str) else r for r in required_roles
    }

    async def dependency(
        current_user: Annotated[User, Depends(_get_current_user)],
    ) -> User:
        user_roles = get_user_roles(current_user)
        if Role.SUPER_ADMIN in user_roles or bool(user_roles & target_roles):
            return current_user
        raise RoleDeniedException(roles=list(target_roles))

    return dependency


def require_permission(
    required_permission: Permission | str,
) -> Callable[[User], Awaitable[User]]:
    """Factory producing a FastAPI dependency enforcing a required permission.

    Args:
        required_permission: The permission required to access the route.

    Returns:
        Callable: Dependency returning current user if authorized.
    """
    target_perm = (
        Permission(required_permission)
        if isinstance(required_permission, str)
        else required_permission
    )

    async def dependency(
        current_user: Annotated[User, Depends(_get_current_user)],
    ) -> User:
        user_perms = get_user_permissions(current_user)
        if target_perm in user_perms:
            return current_user
        raise PermissionDeniedException(permission=target_perm)

    return dependency


def require_any_permission(
    *required_permissions: Permission | str,
) -> Callable[[User], Awaitable[User]]:
    """Factory producing a FastAPI dependency enforcing any of the specified permissions.

    Args:
        *required_permissions: Permissions allowed to access the route.

    Returns:
        Callable: Dependency returning current user if authorized.
    """
    target_perms = {
        Permission(p) if isinstance(p, str) else p for p in required_permissions
    }

    async def dependency(
        current_user: Annotated[User, Depends(_get_current_user)],
    ) -> User:
        user_perms = get_user_permissions(current_user)
        if bool(user_perms & target_perms):
            return current_user
        raise PermissionDeniedException(permissions=list(target_perms))

    return dependency
