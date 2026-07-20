"""Resource ownership and fine-grained authorization policies.

This module implements ownership and resource access rules across roles:
- SUPER_ADMIN & ADMIN: Full access to all resources.
- LAWYER: Access to assigned and owned legal documents and reports.
- PARALEGAL: Read-only access to accessible documents and reports.
- CLIENT: Access strictly limited to owned resources.
"""

from typing import Any

from app.auth.dependencies import get_user_roles
from app.auth.exceptions import OwnershipDeniedException
from app.auth.roles import Role
from app.database.models.user import User


def _is_owner_or_assigned(user: User, resource: Any) -> bool:
    """Helper to check if a user is the owner or assigned to a resource.

    Args:
        user: Authenticated User.
        resource: Target domain object.

    Returns:
        bool: True if user owns or is assigned to the resource.
    """
    user_id = getattr(user, "id", None)
    if user_id is None:
        return False

    # Check direct ownership attributes
    owner_id = getattr(resource, "owner_id", None) or getattr(
        resource, "user_id", None
    )
    if owner_id is not None and str(owner_id) == str(user_id):
        return True

    # Check assignment attributes for lawyers/paralegals
    assigned_id = getattr(resource, "assigned_lawyer_id", None) or getattr(
        resource, "assigned_to", None
    )
    if assigned_id is not None and str(assigned_id) == str(user_id):
        return True

    assigned_list = getattr(resource, "assigned_user_ids", None) or getattr(
        resource, "assigned_lawyers", None
    )
    if assigned_list is not None and isinstance(assigned_list, (list, set, tuple)):
        if any(str(uid) == str(user_id) for uid in assigned_list):
            return True

    return False


def can_view_document(user: User, document: Any) -> bool:
    """Evaluate whether a user can view a specific document.

    Rules:
    - SUPER_ADMIN / ADMIN: Always True.
    - LAWYER: Can view assigned or owned documents.
    - PARALEGAL: Can view assigned or accessible documents (read-only).
    - CLIENT: Can view only own documents.

    Args:
        user: Authenticated User.
        document: Target document object.

    Returns:
        bool: True if viewing is authorized, False otherwise.
    """
    roles = get_user_roles(user)

    if Role.SUPER_ADMIN in roles or Role.ADMIN in roles:
        return True

    if Role.LAWYER in roles or Role.PARALEGAL in roles:
        return _is_owner_or_assigned(user, document)

    if Role.CLIENT in roles:
        return _is_owner_or_assigned(user, document)

    return False


def can_edit_document(user: User, document: Any) -> bool:
    """Evaluate whether a user can edit a specific document.

    Rules:
    - SUPER_ADMIN / ADMIN: Always True.
    - LAWYER: Can edit assigned or owned documents.
    - PARALEGAL: Read only (False).
    - CLIENT: Can edit only own documents (if permitted).

    Args:
        user: Authenticated User.
        document: Target document object.

    Returns:
        bool: True if editing is authorized, False otherwise.
    """
    roles = get_user_roles(user)

    if Role.SUPER_ADMIN in roles or Role.ADMIN in roles:
        return True

    if Role.PARALEGAL in roles:
        return False  # Read only

    if Role.LAWYER in roles or Role.CLIENT in roles:
        return _is_owner_or_assigned(user, document)

    return False


def can_delete_document(user: User, document: Any) -> bool:
    """Evaluate whether a user can delete a specific document.

    Rules:
    - SUPER_ADMIN / ADMIN: Always True.
    - LAWYER: Can delete assigned or owned documents.
    - PARALEGAL: Read only (False).
    - CLIENT: Cannot delete documents (or only own if system allows).

    Args:
        user: Authenticated User.
        document: Target document object.

    Returns:
        bool: True if deletion is authorized, False otherwise.
    """
    roles = get_user_roles(user)

    if Role.SUPER_ADMIN in roles or Role.ADMIN in roles:
        return True

    if Role.PARALEGAL in roles:
        return False

    if Role.LAWYER in roles:
        return _is_owner_or_assigned(user, document)

    if Role.CLIENT in roles:
        return _is_owner_or_assigned(user, document)

    return False


def can_view_report(user: User, report: Any) -> bool:
    """Evaluate whether a user can view a specific report.

    Rules:
    - SUPER_ADMIN / ADMIN: Always True.
    - LAWYER: Can view assigned or owned reports.
    - PARALEGAL: Can view assigned or accessible reports.
    - CLIENT: Can view only own reports.

    Args:
        user: Authenticated User.
        report: Target report object.

    Returns:
        bool: True if viewing is authorized, False otherwise.
    """
    roles = get_user_roles(user)

    if Role.SUPER_ADMIN in roles or Role.ADMIN in roles:
        return True

    if Role.LAWYER in roles or Role.PARALEGAL in roles or Role.CLIENT in roles:
        return _is_owner_or_assigned(user, report)

    return False


def can_delete_report(user: User, report: Any) -> bool:
    """Evaluate whether a user can delete a specific report.

    Rules:
    - SUPER_ADMIN / ADMIN: Always True.
    - LAWYER: Can delete assigned or owned reports.
    - PARALEGAL: Read only (False).
    - CLIENT: Cannot delete reports.

    Args:
        user: Authenticated User.
        report: Target report object.

    Returns:
        bool: True if deletion is authorized, False otherwise.
    """
    roles = get_user_roles(user)

    if Role.SUPER_ADMIN in roles or Role.ADMIN in roles:
        return True

    if Role.PARALEGAL in roles or Role.CLIENT in roles:
        return False

    if Role.LAWYER in roles:
        return _is_owner_or_assigned(user, report)

    return False


# Enforcement Helper Policy Functions
def enforce_view_document(user: User, document: Any) -> None:
    """Enforce document view policy, raising OwnershipDeniedException on failure."""
    if not can_view_document(user, document):
        raise OwnershipDeniedException(
            "Access denied: you do not have permission to view this document."
        )


def enforce_edit_document(user: User, document: Any) -> None:
    """Enforce document edit policy, raising OwnershipDeniedException on failure."""
    if not can_edit_document(user, document):
        raise OwnershipDeniedException(
            "Access denied: you do not have permission to edit this document."
        )


def enforce_delete_document(user: User, document: Any) -> None:
    """Enforce document delete policy, raising OwnershipDeniedException on failure."""
    if not can_delete_document(user, document):
        raise OwnershipDeniedException(
            "Access denied: you do not have permission to delete this document."
        )


def enforce_view_report(user: User, report: Any) -> None:
    """Enforce report view policy, raising OwnershipDeniedException on failure."""
    if not can_view_report(user, report):
        raise OwnershipDeniedException(
            "Access denied: you do not have permission to view this report."
        )


def enforce_delete_report(user: User, report: Any) -> None:
    """Enforce report delete policy, raising OwnershipDeniedException on failure."""
    if not can_delete_report(user, report):
        raise OwnershipDeniedException(
            "Access denied: you do not have permission to delete this report."
        )
