"""RBAC Authorization Module.

Provides decoupled role and permission checking, FastAPI dependency factories,
custom exceptions, and resource ownership policies.
"""

from app.auth.dependencies import (
    get_user_permissions,
    get_user_roles,
    require_any_permission,
    require_any_role,
    require_permission,
    require_role,
)
from app.auth.exceptions import (
    OwnershipDeniedException,
    PermissionDeniedException,
    RoleDeniedException,
)
from app.auth.permissions import ROLE_PERMISSIONS, Permission
from app.auth.policies import (
    can_delete_document,
    can_delete_report,
    can_edit_document,
    can_view_document,
    can_view_report,
    enforce_delete_document,
    enforce_delete_report,
    enforce_edit_document,
    enforce_view_document,
    enforce_view_report,
)
from app.auth.roles import Role

__all__ = [
    # Enums & Mappings
    "Role",
    "Permission",
    "ROLE_PERMISSIONS",
    # Exceptions
    "PermissionDeniedException",
    "RoleDeniedException",
    "OwnershipDeniedException",
    # Dependencies & Helpers
    "require_role",
    "require_any_role",
    "require_permission",
    "require_any_permission",
    "get_user_roles",
    "get_user_permissions",
    # Policies
    "can_view_document",
    "can_edit_document",
    "can_delete_document",
    "can_view_report",
    "can_delete_report",
    "enforce_view_document",
    "enforce_edit_document",
    "enforce_delete_document",
    "enforce_view_report",
    "enforce_delete_report",
]
