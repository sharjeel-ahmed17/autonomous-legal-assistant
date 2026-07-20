from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Header
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.core.exceptions import UnauthorizedException
from app.database.models.user import User
from app.services.auth_service import AuthService
from app.services.user_service import UserService


from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer(auto_error=False)


async def get_auth_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AsyncGenerator[AuthService, None]:
    yield AuthService(session)


async def get_user_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AsyncGenerator[UserService, None]:
    yield UserService(session)


async def _get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)] = None,
    authorization: Annotated[str | None, Header()] = None,
    auth_service: Annotated[AuthService, Depends(get_auth_service)] = None,
) -> User:
    token: str | None = None

    if credentials and credentials.credentials:
        token = credentials.credentials
    elif authorization and authorization.strip():
        auth_str = authorization.strip()
        if auth_str.lower().startswith("bearer "):
            token = auth_str[7:].strip()
        else:
            token = auth_str

    if not token:
        raise UnauthorizedException(
            "Authorization header with Bearer token is required. Format: Bearer <access_token>"
        )

    return await auth_service.get_current_user(token)


CurrentUser = Annotated[User, Depends(_get_current_user)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]

