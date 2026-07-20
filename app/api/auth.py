from uuid import UUID

from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.dependencies import AuthServiceDep, CurrentUser, UserServiceDep
from app.database.schemas.api_key import ApiKeyCreate, ApiKeyCreated, ApiKeyRead
from app.database.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


@router.post("/register", response_model=UserRead, status_code=201)
async def register(
    payload: UserCreate,
    auth_service: AuthServiceDep,
) -> UserRead:
    return await auth_service.register_user(payload)


@router.post("/login")
async def login(
    payload: LoginRequest,
    request: Request,
    auth_service: AuthServiceDep,
) -> dict:
    return await auth_service.login(
        email=payload.email,
        password=payload.password,
        device_info=request.headers.get("user-agent"),
        ip_address=request.client.host if request.client else None,
    )


@router.post("/refresh")
async def refresh(
    payload: RefreshRequest,
    request: Request,
    auth_service: AuthServiceDep,
) -> dict:
    return await auth_service.refresh_access_token(
        refresh_token=payload.refresh_token,
        device_info=request.headers.get("user-agent"),
        ip_address=request.client.host if request.client else None,
    )


@router.post("/logout", status_code=204)
async def logout(
    payload: LogoutRequest,
    auth_service: AuthServiceDep,
) -> None:
    await auth_service.logout(payload.refresh_token)


@router.get("/me", response_model=UserRead)
async def get_me(
    user: CurrentUser,
) -> UserRead:
    return UserRead(
        id=user.id,
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.post("/change-password", status_code=204)
async def change_password(
    payload: ChangePasswordRequest,
    user: CurrentUser,
    user_service: UserServiceDep,
) -> None:
    await user_service.change_password(
        user_id=user.id,
        current_password=payload.current_password,
        new_password=payload.new_password,
    )


@router.post("/api-keys", response_model=ApiKeyCreated, status_code=201)
async def create_api_key(
    payload: ApiKeyCreate,
    user: CurrentUser,
    auth_service: AuthServiceDep,
) -> ApiKeyCreated:
    return await auth_service.create_api_key(
        user=user,
        name=payload.name,
        scopes=payload.scopes,
        expires_at=payload.expires_at,
    )


@router.get("/api-keys", response_model=list[ApiKeyRead])
async def list_api_keys(
    user: CurrentUser,
    auth_service: AuthServiceDep,
) -> list[ApiKeyRead]:
    return await auth_service.list_api_keys(user)


@router.delete("/api-keys/{key_id}", status_code=204)
async def revoke_api_key(
    key_id: UUID,
    user: CurrentUser,
    auth_service: AuthServiceDep,
) -> None:
    await auth_service.revoke_api_key(user, str(key_id))


@router.get("/sessions")
async def list_sessions(
    user: CurrentUser,
    auth_service: AuthServiceDep,
) -> list[dict]:
    tokens = await auth_service.list_refresh_tokens(user)
    return [
        {
            "id": str(t.id),
            "created_at": t.created_at.isoformat(),
            "expires_at": t.expires_at.isoformat(),
            "is_revoked": t.is_revoked,
            "device_info": t.device_info,
            "ip_address": t.ip_address,
        }
        for t in tokens
    ]


@router.delete("/sessions/{token_id}", status_code=204)
async def revoke_session(
    token_id: UUID,
    user: CurrentUser,
    auth_service: AuthServiceDep,
) -> None:
    await auth_service.revoke_refresh_token(user, str(token_id))
