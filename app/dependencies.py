from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Header
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.core.exceptions import UnauthorizedException
from app.database.models.user import User
from app.services.auth_service import AuthService
from app.services.user_service import UserService


async def get_auth_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AsyncGenerator[AuthService, None]:
    yield AuthService(session)


async def get_user_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AsyncGenerator[UserService, None]:
    yield UserService(session)


async def _get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    auth_service: Annotated[AuthService, Depends(get_auth_service)] = None,
) -> User:
    if not authorization:
        raise UnauthorizedException("Authorization header is required.")

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise UnauthorizedException(
            "Invalid authorization header format. Use: Bearer <token>"
        )

    return await auth_service.get_current_user(token)


CurrentUser = Annotated[User, Depends(_get_current_user)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
