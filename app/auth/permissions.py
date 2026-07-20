"""Permission definitions and role-to-permission mappings.

This module defines granular application permissions using Python StrEnum
and establishes the mapping between roles and permission sets.
"""

from enum import StrEnum

from app.auth.roles import Role


class Permission(StrEnum):
    """Enumeration of granular system permissions.

    Permissions follow the standard `resource:action` naming convention.
    """

    # User Management
    USERS_CREATE = "users:create"
    USERS_READ = "users:read"
    USERS_UPDATE = "users:update"
    USERS_DELETE = "users:delete"

    # Document Management
    DOCUMENTS_CREATE = "documents:create"
    DOCUMENTS_READ = "documents:read"
    DOCUMENTS_UPDATE = "documents:update"
    DOCUMENTS_DELETE = "documents:delete"

    # Chat & Assistant
    CHAT_USE = "chat:use"

    # Reports
    REPORTS_CREATE = "reports:create"
    REPORTS_READ = "reports:read"
    REPORTS_DELETE = "reports:delete"

    # Contracts & Intelligence
    CONTRACTS_ANALYZE = "contracts:analyze"

    # Agents & Workflows
    AGENTS_EXECUTE = "agents:execute"

    # Audit & Administration
    AUDIT_READ = "audit:read"
    MCP_EXECUTE = "mcp:execute"
    ADMIN_ACCESS = "admin:access"


# Complete RBAC Role-to-Permission Mapping
ROLE_PERMISSIONS: dict[Role, set[Permission]] = {
    # SUPER_ADMIN gets every single permission
    Role.SUPER_ADMIN: set(Permission),
    # ADMIN gets administration, audit, user management, and document oversight
    Role.ADMIN: {
        Permission.ADMIN_ACCESS,
        Permission.USERS_CREATE,
        Permission.USERS_READ,
        Permission.USERS_UPDATE,
        Permission.USERS_DELETE,
        Permission.DOCUMENTS_READ,
        Permission.DOCUMENTS_UPDATE,
        Permission.DOCUMENTS_DELETE,
        Permission.REPORTS_READ,
        Permission.REPORTS_DELETE,
        Permission.AUDIT_READ,
        Permission.CHAT_USE,
        Permission.MCP_EXECUTE,
    },
    # LAWYER gets full legal workflow capabilities
    Role.LAWYER: {
        Permission.DOCUMENTS_CREATE,
        Permission.DOCUMENTS_READ,
        Permission.DOCUMENTS_UPDATE,
        Permission.DOCUMENTS_DELETE,
        Permission.CONTRACTS_ANALYZE,
        Permission.REPORTS_CREATE,
        Permission.REPORTS_READ,
        Permission.REPORTS_DELETE,
        Permission.CHAT_USE,
        Permission.AGENTS_EXECUTE,
    },
    # PARALEGAL gets document upload, reading, and chat assistance
    Role.PARALEGAL: {
        Permission.DOCUMENTS_CREATE,
        Permission.DOCUMENTS_READ,
        Permission.CHAT_USE,
    },
    # CLIENT gets read-only access to their own documents and chat
    Role.CLIENT: {
        Permission.DOCUMENTS_READ,
        Permission.CHAT_USE,
    },
}
