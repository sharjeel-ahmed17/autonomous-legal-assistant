from datetime import UTC, datetime, timedelta

from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.core.exceptions import (
    ConflictException,
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
)
from app.core.security import (
    create_access_token,
    decode_access_token,
    generate_api_key,
    generate_secure_token,
    hash_password,
    verify_password,
)
from app.database.models.api_key import ApiKey
from app.database.models.refresh_token import RefreshToken
from app.database.models.user import User
from app.database.repositories.api_key import ApiKeyRepository
from app.database.repositories.refresh_token import RefreshTokenRepository
from app.database.repositories.user import UserRepository
from app.database.schemas.api_key import ApiKeyCreated, ApiKeyRead
from app.database.schemas.refresh_token import RefreshTokenRead
from app.database.schemas.user import UserCreate, UserRead

REFRESH_TOKEN_EXPIRE_DAYS = 30


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository()
        self.refresh_token_repo = RefreshTokenRepository()
        self.api_key_repo = ApiKeyRepository()

    async def register_user(self, payload: UserCreate) -> UserRead:
        existing = await self.user_repo.get_by_email(self.session, payload.email)
        if existing:
            raise ConflictException("A user with this email already exists.")

        user = User(
            email=payload.email,
            username=payload.username,
            hashed_password=hash_password(payload.password),
            full_name=payload.full_name,
        )
        user = await self.user_repo.create(self.session, user)
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

    async def authenticate_user(self, email: str, password: str) -> User:
        user = await self.user_repo.get_by_email(self.session, email)
        if not user:
            raise UnauthorizedException("Invalid email or password.")
        if not user.is_active:
            raise ForbiddenException("Account is deactivated.")
        if not verify_password(password, user.hashed_password):
            raise UnauthorizedException("Invalid email or password.")
        return user

    async def login(
        self,
        email: str,
        password: str,
        device_info: str | None = None,
        ip_address: str | None = None,
    ) -> dict:
        user = await self.authenticate_user(email, password)
        return await self._generate_tokens(user, device_info, ip_address)

    async def refresh_access_token(
        self,
        refresh_token: str,
        device_info: str | None = None,
        ip_address: str | None = None,
    ) -> dict:
        token_hash = hash_password(refresh_token)
        stored = await self.refresh_token_repo.get_by_token_hash(
            self.session, token_hash
        )
        if not stored or stored.is_revoked:
            raise UnauthorizedException("Invalid or revoked refresh token.")
        if stored.expires_at < datetime.now(UTC):
            raise UnauthorizedException("Refresh token has expired.")

        stored.is_revoked = True
        await self.refresh_token_repo.update(self.session, stored)

        user = await self.user_repo.get_by_id(self.session, stored.user_id)
        if not user or not user.is_active:
            raise UnauthorizedException("User not found or inactive.")

        return await self._generate_tokens(user, device_info, ip_address)

    async def logout(self, refresh_token: str) -> None:
        token_hash = hash_password(refresh_token)
        stored = await self.refresh_token_repo.get_by_token_hash(
            self.session, token_hash
        )
        if stored:
            stored.is_revoked = True
            await self.refresh_token_repo.update(self.session, stored)

    async def get_current_user(self, token: str) -> User:
        try:
            payload = decode_access_token(token)
        except ValueError as exc:
            raise UnauthorizedException(str(exc))

        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedException("Invalid token payload.")

        user = await self.user_repo.get_by_id(self.session, user_id)
        if not user:
            raise NotFoundException("User not found.")
        if not user.is_active:
            raise ForbiddenException("Account is deactivated.")
        return user

    async def create_api_key(
        self,
        user: User,
        name: str,
        scopes: str | None = None,
        expires_at: datetime | None = None,
    ) -> ApiKeyCreated:
        raw_key = generate_api_key()
        key_hash = hash_password(raw_key)
        key_prefix = raw_key[:8]

        api_key = ApiKey(
            user_id=user.id,
            key_hash=key_hash,
            key_prefix=key_prefix,
            name=name,
            scopes=scopes,
            expires_at=expires_at,
        )
        api_key = await self.api_key_repo.create(self.session, api_key)

        return ApiKeyCreated(
            id=api_key.id,
            user_id=api_key.user_id,
            key_prefix=api_key.key_prefix,
            name=api_key.name,
            scopes=api_key.scopes,
            is_active=api_key.is_active,
            last_used_at=api_key.last_used_at,
            expires_at=api_key.expires_at,
            created_at=api_key.created_at,
            updated_at=api_key.updated_at,
            raw_key=raw_key,
        )

    async def validate_api_key(self, raw_key: str) -> ApiKey:
        all_keys = await self.api_key_repo.get_all(self.session)
        for api_key in all_keys:
            if verify_password(raw_key, api_key.key_hash):
                if not api_key.is_active:
                    raise ForbiddenException("API key is deactivated.")
                if api_key.expires_at and api_key.expires_at < datetime.now(UTC):
                    raise ForbiddenException("API key has expired.")
                api_key.last_used_at = datetime.now(UTC)
                await self.api_key_repo.update(self.session, api_key)
                return api_key
        raise UnauthorizedException("Invalid API key.")

    async def list_api_keys(self, user: User) -> list[ApiKeyRead]:
        keys = await self.api_key_repo.get_by_user(self.session, user.id)
        return [
            ApiKeyRead(
                id=k.id,
                user_id=k.user_id,
                key_prefix=k.key_prefix,
                name=k.name,
                scopes=k.scopes,
                is_active=k.is_active,
                last_used_at=k.last_used_at,
                expires_at=k.expires_at,
                created_at=k.created_at,
                updated_at=k.updated_at,
            )
            for k in keys
        ]

    async def revoke_api_key(self, user: User, key_id: str) -> None:
        api_key = await self.api_key_repo.get_by_id(self.session, key_id)
        if not api_key or api_key.user_id != user.id:
            raise NotFoundException("API key not found.")
        api_key.is_active = False
        await self.api_key_repo.update(self.session, api_key)

    async def list_refresh_tokens(self, user: User) -> list[RefreshTokenRead]:
        tokens = await self.refresh_token_repo.get_by_user(self.session, user.id)
        return [
            RefreshTokenRead(
                id=t.id,
                user_id=t.user_id,
                expires_at=t.expires_at,
                is_revoked=t.is_revoked,
                device_info=t.device_info,
                ip_address=t.ip_address,
                created_at=t.created_at,
                updated_at=t.updated_at,
            )
            for t in tokens
        ]

    async def revoke_refresh_token(self, user: User, token_id: str) -> None:
        token = await self.refresh_token_repo.get_by_id(self.session, token_id)
        if not token or token.user_id != user.id:
            raise NotFoundException("Refresh token not found.")
        token.is_revoked = True
        await self.refresh_token_repo.update(self.session, token)

    async def _generate_tokens(
        self,
        user: User,
        device_info: str | None = None,
        ip_address: str | None = None,
    ) -> dict:
        access_token = create_access_token(subject=str(user.id))
        raw_refresh = generate_secure_token(48)
        refresh_token_hash = hash_password(raw_refresh)

        refresh_record = RefreshToken(
            user_id=user.id,
            token_hash=refresh_token_hash,
            expires_at=datetime.now(UTC) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
            device_info=device_info,
            ip_address=ip_address,
        )
        await self.refresh_token_repo.create(self.session, refresh_record)

        return {
            "access_token": access_token,
            "refresh_token": raw_refresh,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": UserRead(
                id=user.id,
                email=user.email,
                username=user.username,
                full_name=user.full_name,
                is_active=user.is_active,
                is_superuser=user.is_superuser,
                created_at=user.created_at,
                updated_at=user.updated_at,
            ),
        }
