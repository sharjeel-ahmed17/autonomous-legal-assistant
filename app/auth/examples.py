"""Example FastAPI routes demonstrating RBAC authorization dependencies and policies.

This file illustrates standard usages of:
1. Role-based endpoint guards (`require_role`, `require_any_role`)
2. Permission-based endpoint guards (`require_permission`, `require_any_permission`)
3. Fine-grained resource ownership policies (`enforce_view_document`, `can_edit_document`, etc.)
"""

from uuid import UUID

from fastapi import APIRouter, Depends

from app.auth import (
    Permission,
    Role,
    can_edit_document,
    enforce_delete_document,
    enforce_view_document,
    require_any_permission,
    require_any_role,
    require_permission,
    require_role,
)
from app.database.models.user import User

router = APIRouter(prefix="/examples", tags=["Authorization Examples"])


# Example 1: Require specific Role (ADMIN)
@router.get(
    "/admin-dashboard",
    dependencies=[Depends(require_role(Role.ADMIN))],
)
async def get_admin_dashboard(
    current_user: User = Depends(require_role(Role.ADMIN)),
) -> dict[str, str]:
    """Endpoint accessible only by users with ADMIN or SUPER_ADMIN roles."""
    return {"message": f"Welcome Admin {current_user.username}"}


# Example 2: Require any of multiple Roles (LAWYER or PARALEGAL)
@router.get("/legal-workspace")
async def get_legal_workspace(
    current_user: User = Depends(require_any_role(Role.LAWYER, Role.PARALEGAL)),
) -> dict[str, str]:
    """Endpoint accessible by LAWYER, PARALEGAL, or SUPER_ADMIN."""
    return {"message": f"Access granted for user {current_user.username}"}


# Example 3: Require specific Permission (documents:create)
@router.post("/documents")
async def create_document(
    current_user: User = Depends(require_permission(Permission.DOCUMENTS_CREATE)),
) -> dict[str, str]:
    """Endpoint enforcing single permission check."""
    return {"message": "Document created successfully"}


# Example 4: Require any of multiple Permissions (contracts:analyze or agents:execute)
@router.post("/contracts/analyze")
async def analyze_contract(
    current_user: User = Depends(
        require_any_permission(
            Permission.CONTRACTS_ANALYZE, Permission.AGENTS_EXECUTE
        )
    ),
) -> dict[str, str]:
    """Endpoint enforcing any of multiple permission checks."""
    return {"message": "Contract analysis initiated"}


# Example 5: Resource ownership policy check in route
@router.get("/documents/{document_id}")
async def read_document_with_policy(
    document_id: UUID,
    current_user: User = Depends(require_permission(Permission.DOCUMENTS_READ)),
) -> dict[str, str]:
    """Endpoint combining permission dependency with ownership policy enforcement."""
    # Simulated database lookup (e.g. document = await document_service.get(document_id))
    mock_document = type(
        "MockDocument", (), {"id": document_id, "owner_id": current_user.id}
    )()

    # Enforce resource-level viewing policy (raises OwnershipDeniedException if invalid)
    enforce_view_document(current_user, mock_document)

    # Check edit permissions dynamically if returning edit action metadata
    editable = can_edit_document(current_user, mock_document)

    return {
        "document_id": str(document_id),
        "status": "accessed",
        "can_edit": str(editable),
    }


# Example 6: Resource deletion with policy enforcement
@router.delete("/documents/{document_id}")
async def delete_document_with_policy(
    document_id: UUID,
    current_user: User = Depends(require_permission(Permission.DOCUMENTS_DELETE)),
) -> dict[str, str]:
    """Endpoint enforcing deletion permission & ownership policy."""
    mock_document = type(
        "MockDocument", (), {"id": document_id, "owner_id": current_user.id}
    )()

    enforce_delete_document(current_user, mock_document)

    return {"message": f"Document {document_id} deleted successfully"}
