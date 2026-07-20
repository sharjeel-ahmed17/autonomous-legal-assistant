"""Unit tests for RBAC authorization module."""

import pytest
from fastapi import status

from app.auth import (
    Permission,
    Role,
    ROLE_PERMISSIONS,
    OwnershipDeniedException,
    PermissionDeniedException,
    RoleDeniedException,
    can_delete_document,
    can_edit_document,
    can_view_document,
    enforce_view_document,
    get_user_permissions,
    get_user_roles,
    require_permission,
    require_role,
)
from app.database.models.role import Role as DBRole
from app.database.models.user import User


class DummyResource:
    def __init__(self, owner_id=None, user_id=None, assigned_lawyer_id=None):
        self.owner_id = owner_id
        self.user_id = user_id
        self.assigned_lawyer_id = assigned_lawyer_id


def test_roles_and_permissions_enum():
    assert Role.SUPER_ADMIN == "super_admin"
    assert Role.ADMIN == "admin"
    assert Role.LAWYER == "lawyer"
    assert Role.PARALEGAL == "paralegal"
    assert Role.CLIENT == "client"

    assert Permission.USERS_CREATE == "users:create"
    assert Permission.DOCUMENTS_READ == "documents:read"
    assert Permission.CHAT_USE == "chat:use"


def test_role_permissions_mapping():
    assert set(Permission).issubset(ROLE_PERMISSIONS[Role.SUPER_ADMIN])
    assert Permission.ADMIN_ACCESS in ROLE_PERMISSIONS[Role.ADMIN]
    assert Permission.CONTRACTS_ANALYZE in ROLE_PERMISSIONS[Role.LAWYER]
    assert Permission.DOCUMENTS_CREATE in ROLE_PERMISSIONS[Role.PARALEGAL]
    assert Permission.DOCUMENTS_READ in ROLE_PERMISSIONS[Role.CLIENT]
    assert Permission.USERS_DELETE not in ROLE_PERMISSIONS[Role.CLIENT]


def test_get_user_roles_and_permissions():
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hash",
        is_superuser=False,
    )
    user.roles = [DBRole(name="Lawyer", codename="lawyer")]

    roles = get_user_roles(user)
    assert Role.LAWYER in roles

    perms = get_user_permissions(user)
    assert Permission.DOCUMENTS_CREATE in perms
    assert Permission.CONTRACTS_ANALYZE in perms


def test_superuser_roles_and_permissions():
    superuser = User(
        email="admin@example.com",
        username="adminuser",
        hashed_password="hash",
        is_superuser=True,
    )

    roles = get_user_roles(superuser)
    assert Role.SUPER_ADMIN in roles

    perms = get_user_permissions(superuser)
    assert perms == set(Permission)


@pytest.mark.anyio
async def test_require_role_dependency():
    user = User(
        email="lawyer@example.com",
        username="lawyer",
        hashed_password="hash",
        is_superuser=False,
    )
    user.roles = [DBRole(name="Lawyer", codename="lawyer")]

    dep_lawyer = require_role(Role.LAWYER)
    res = await dep_lawyer(current_user=user)
    assert res == user

    dep_admin = require_role(Role.ADMIN)
    with pytest.raises(RoleDeniedException) as exc_info:
        await dep_admin(current_user=user)
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.anyio
async def test_require_permission_dependency():
    user = User(
        email="client@example.com",
        username="client",
        hashed_password="hash",
        is_superuser=False,
    )
    user.roles = [DBRole(name="Client", codename="client")]

    dep_read = require_permission(Permission.DOCUMENTS_READ)
    res = await dep_read(current_user=user)
    assert res == user

    dep_delete = require_permission(Permission.DOCUMENTS_DELETE)
    with pytest.raises(PermissionDeniedException) as exc_info:
        await dep_delete(current_user=user)
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN


def test_policies():
    admin = User(email="admin@e.com", username="admin", hashed_password="h", is_superuser=True)
    client = User(email="client@e.com", username="client", hashed_password="h", is_superuser=False)
    client.id = "11111111-1111-1111-1111-111111111111"
    client.roles = [DBRole(name="Client", codename="client")]

    doc_own = DummyResource(owner_id="11111111-1111-1111-1111-111111111111")
    doc_other = DummyResource(owner_id="22222222-2222-2222-2222-222222222222")

    # Admin checks
    assert can_view_document(admin, doc_other) is True
    assert can_edit_document(admin, doc_other) is True
    assert can_delete_document(admin, doc_other) is True

    # Client checks
    assert can_view_document(client, doc_own) is True
    assert can_view_document(client, doc_other) is False

    enforce_view_document(client, doc_own)
    with pytest.raises(OwnershipDeniedException):
        enforce_view_document(client, doc_other)
