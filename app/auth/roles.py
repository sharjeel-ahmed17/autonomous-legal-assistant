"""Role definitions for Role-Based Access Control (RBAC).

This module defines system user roles using standard Python StrEnum.
"""

from enum import StrEnum


class Role(StrEnum):
    """Enumeration of user roles within the application.

    Attributes:
        SUPER_ADMIN: Full system access and privileges across all resources.
        ADMIN: Administrative access for platform management and user oversight.
        LAWYER: Full access to legal operations, documents, contracts, and reports.
        PARALEGAL: Document upload, viewing, and assistance capabilities.
        CLIENT: Restricted access limited to personal documents and chat.
    """

    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    LAWYER = "lawyer"
    PARALEGAL = "paralegal"
    CLIENT = "client"
