"""Integration tests for all FastAPI application routes and RBAC authorization guards."""

from datetime import datetime
from unittest.mock import AsyncMock
from uuid import uuid4

from fastapi.testclient import TestClient

from app.database.models.role import Role as DBRole
from app.database.models.user import User
from app.dependencies import _get_current_user, get_auth_service, get_user_service
from app.main import app

client = TestClient(app)


# --- Helper User Factories ---
def create_mock_user(role_name: str, is_superuser: bool = False) -> User:
    """Create a mock user instance with specified role."""
    now = datetime.now()
    u = User(
        id=uuid4(),
        email=f"{role_name}@example.com",
        username=f"user_{role_name}",
        full_name=f"Mock {role_name.title()}",
        hashed_password="hashedpassword",
        is_superuser=is_superuser,
        created_at=now,
        updated_at=now,
    )
    u.roles = [DBRole(name=role_name.title(), codename=role_name)]
    return u


# --- 1. Root & Health Route Tests ---
def test_root_endpoint():
    """Test public root endpoint GET /."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


# --- 2. Unauthenticated Access Tests (Expecting 401 Unauthorized) ---
def test_unauthenticated_protected_routes():
    """Test that accessing protected endpoints without Bearer token returns 401."""
    # Auth protected endpoints
    res_me = client.get("/api/v1/auth/me")
    assert res_me.status_code == 401

    res_keys = client.get("/api/v1/auth/api-keys")
    assert res_keys.status_code == 401

    # User management protected endpoints
    res_users = client.get("/api/v1/users")
    assert res_users.status_code == 401

    # Example RBAC protected endpoints
    res_admin = client.get("/api/v1/examples/admin-dashboard")
    assert res_admin.status_code == 401


# --- 3. Authorization Role & Permission Guard Tests ---
def test_client_role_forbidden_access():
    """Test that a CLIENT user is rejected with 403 on admin & lawyer routes."""
    client_user = create_mock_user("client")
    app.dependency_overrides[_get_current_user] = lambda: client_user

    try:
        # Client trying to access admin dashboard -> 403
        res_admin = client.get("/api/v1/examples/admin-dashboard")
        assert res_admin.status_code == 403
        assert "Access denied: required role 'admin'" in res_admin.json()["detail"]

        # Client trying to access legal workspace -> 403
        res_legal = client.get("/api/v1/examples/legal-workspace")
        assert res_legal.status_code == 403

        # Client trying to analyze contracts -> 403
        res_contract = client.post("/api/v1/examples/contracts/analyze")
        assert res_contract.status_code == 403
        assert "Permission denied" in res_contract.json()["detail"]
    finally:
        app.dependency_overrides.clear()


def test_admin_role_authorized_access():
    """Test that an ADMIN user is granted access to admin routes."""
    admin_user = create_mock_user("admin")
    app.dependency_overrides[_get_current_user] = lambda: admin_user

    try:
        res_admin = client.get("/api/v1/examples/admin-dashboard")
        assert res_admin.status_code == 200
        assert res_admin.json() == {"message": f"Welcome Admin {admin_user.username}"}
    finally:
        app.dependency_overrides.clear()


def test_lawyer_role_authorized_access():
    """Test that a LAWYER user can access legal workspace, contracts, and documents."""
    lawyer_user = create_mock_user("lawyer")
    app.dependency_overrides[_get_current_user] = lambda: lawyer_user

    try:
        res_workspace = client.get("/api/v1/examples/legal-workspace")
        assert res_workspace.status_code == 200

        res_contract = client.post("/api/v1/examples/contracts/analyze")
        assert res_contract.status_code == 200
        assert res_contract.json() == {"message": "Contract analysis initiated"}

        res_doc_create = client.post("/api/v1/examples/documents")
        assert res_doc_create.status_code == 200
    finally:
        app.dependency_overrides.clear()


def test_document_policy_enforcement():
    """Test document ownership policy enforcement for viewing and deleting."""
    user = create_mock_user("lawyer")
    app.dependency_overrides[_get_current_user] = lambda: user
    doc_id = str(uuid4())

    try:
        # Lawyer reading accessible document -> 200
        res_read = client.get(f"/api/v1/examples/documents/{doc_id}")
        assert res_read.status_code == 200
        assert res_read.json()["document_id"] == doc_id

        # Lawyer deleting document -> 200
        res_del = client.delete(f"/api/v1/examples/documents/{doc_id}")
        assert res_del.status_code == 200
    finally:
        app.dependency_overrides.clear()


# --- 4. User API Route Integration Tests ---
def test_user_api_routes():
    """Test /api/v1/users endpoints with mock UserService."""
    admin_user = create_mock_user("admin")
    now = datetime.now()
    mock_service = AsyncMock()
    mock_service.list_users.return_value = {
        "items": [],
        "total": 0,
        "page": 1,
        "page_size": 20,
        "total_pages": 0,
    }
    mock_service.get_by_id.return_value = {
        "id": str(admin_user.id),
        "email": admin_user.email,
        "username": admin_user.username,
        "full_name": admin_user.full_name,
        "is_active": True,
        "is_superuser": False,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
    }

    app.dependency_overrides[_get_current_user] = lambda: admin_user
    app.dependency_overrides[get_user_service] = lambda: mock_service

    try:
        # GET /api/v1/users
        res_list = client.get("/api/v1/users")
        assert res_list.status_code == 200

        # GET /api/v1/users/{id}
        res_get = client.get(f"/api/v1/users/{admin_user.id}")
        assert res_get.status_code == 200
    finally:
        app.dependency_overrides.clear()


# --- 5. Auth API Route Integration Tests ---
def test_auth_api_routes():
    """Test /api/v1/auth endpoints."""
    user = create_mock_user("client")
    mock_auth_service = AsyncMock()
    mock_auth_service.login.return_value = {
        "access_token": "mock_jwt",
        "token_type": "bearer",
    }

    app.dependency_overrides[_get_current_user] = lambda: user
    app.dependency_overrides[get_auth_service] = lambda: mock_auth_service

    try:
        # POST /api/v1/auth/login
        res_login = client.post(
            "/api/v1/auth/login",
            json={"email": "client@example.com", "password": "password123"},
        )
        assert res_login.status_code == 200
        assert res_login.json()["access_token"] == "mock_jwt"

        # GET /api/v1/auth/me
        res_me = client.get("/api/v1/auth/me")
        assert res_me.status_code == 200
        assert res_me.json()["email"] == "client@example.com"
    finally:
        app.dependency_overrides.clear()
