"""Custom authorization exceptions for the RBAC authorization module.

All exceptions inherit from FastAPI's HTTPException and return HTTP status 403.
"""

from collections.abc import Sequence

from fastapi import HTTPException, status

from app.auth.permissions import Permission
from app.auth.roles import Role


class PermissionDeniedException(HTTPException):
    """Exception raised when a user lacks a required permission."""

    def __init__(
        self,
        permission: Permission | str | None = None,
        permissions: Sequence[Permission | str] | None = None,
        detail: str | None = None,
    ) -> None:
        """Initialize PermissionDeniedException.

        Args:
            permission: The single missing permission (optional).
            permissions: A sequence of missing permissions (optional).
            detail: Custom error message detail (optional).
        """
        if detail is None:
            if permission:
                detail = f"Permission denied: required permission '{permission}'."
            elif permissions:
                formatted_perms = ", ".join(f"'{p}'" for p in permissions)
                detail = (
                    f"Permission denied: required any of permissions [{formatted_perms}]."
                )
            else:
                detail = "Permission denied: insufficient permissions."

        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class RoleDeniedException(HTTPException):
    """Exception raised when a user lacks a required role."""

    def __init__(
        self,
        role: Role | str | None = None,
        roles: Sequence[Role | str] | None = None,
        detail: str | None = None,
    ) -> None:
        """Initialize RoleDeniedException.

        Args:
            role: The single missing required role (optional).
            roles: A sequence of missing required roles (optional).
            detail: Custom error message detail (optional).
        """
        if detail is None:
            if role:
                detail = f"Access denied: required role '{role}'."
            elif roles:
                formatted_roles = ", ".join(f"'{r}'" for r in roles)
                detail = f"Access denied: required any of roles [{formatted_roles}]."
            else:
                detail = "Access denied: insufficient role privileges."

        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class OwnershipDeniedException(HTTPException):
    """Exception raised when resource ownership check fails."""

    def __init__(
        self,
        detail: str = (
            "Access denied: you do not have ownership or access rights for this resource."
        ),
    ) -> None:
        """Initialize OwnershipDeniedException.

        Args:
            detail: Custom error message detail.
        """
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )
