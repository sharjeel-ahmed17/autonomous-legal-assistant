from __future__ import annotations

from datetime import UTC, datetime, timedelta
from hashlib import sha256
from typing import Any

from app.core.config import settings
from app.core.security import ALGORITHM
from app.core.exceptions import UnauthorizedException

try:
    import jwt
    from jwt import ExpiredSignatureError, InvalidTokenError
except ImportError:
    jwt = None  # type: ignore[assignment]
    ExpiredSignatureError = Exception
    InvalidTokenError = Exception

try:
    import redis.asyncio as aioredis
except ImportError:
    aioredis = None  # type: ignore[assignment]


class TokenService:
    def __init__(self, redis_client: aioredis.Redis | None = None):
        self._redis = redis_client
        self._blacklist_prefix = "token:blacklist:"

    @property
    def _redis_available(self) -> bool:
        return self._redis is not None

    def create_token(
        self,
        subject: str,
        expires_delta: timedelta | None = None,
        additional_claims: dict[str, Any] | None = None,
        token_type: str = "access",
    ) -> str:
        expire = datetime.now(UTC) + (
            expires_delta
            or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        payload: dict[str, Any] = {
            "sub": subject,
            "exp": expire,
            "iat": datetime.now(UTC),
            "type": token_type,
        }

        if additional_claims:
            payload.update(additional_claims)

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=ALGORITHM,
        )

    def decode_token(self, token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[ALGORITHM],
            )
            return payload
        except ExpiredSignatureError:
            raise UnauthorizedException("Token has expired.")
        except InvalidTokenError:
            raise UnauthorizedException("Invalid token.")

    def get_subject(self, token: str) -> str:
        payload = self.decode_token(token)
        subject = payload.get("sub")
        if not subject:
            raise UnauthorizedException("Token missing subject claim.")
        return subject

    def get_token_type(self, token: str) -> str | None:
        payload = self.decode_token(token)
        return payload.get("type")

    def get_expiry(self, token: str) -> datetime | None:
        payload = self.decode_token(token)
        exp = payload.get("exp")
        if exp:
            return datetime.fromtimestamp(exp, tz=UTC)
        return None

    def get_remaining_ttl(self, token: str) -> int:
        exp = self.get_expiry(token)
        if not exp:
            return 0
        remaining = int((exp - datetime.now(UTC)).total_seconds())
        return max(remaining, 0)

    def is_expired(self, token: str) -> bool:
        return self.get_remaining_ttl(token) <= 0

    def has_claim(self, token: str, claim: str) -> bool:
        payload = self.decode_token(token)
        return claim in payload

    def get_claim(self, token: str, claim: str, default: Any = None) -> Any:
        payload = self.decode_token(token)
        return payload.get(claim, default)

    def validate_token(self, token: str, expected_type: str | None = None) -> dict[str, Any]:
        payload = self.decode_token(token)

        if expected_type and payload.get("type") != expected_type:
            raise UnauthorizedException(
                f"Invalid token type. Expected '{expected_type}'."
            )

        return payload

    def _token_key(self, token: str) -> str:
        digest = sha256(token.encode()).hexdigest()
        return f"{self._blacklist_prefix}{digest}"

    async def blacklist_token(
        self,
        token: str,
        expires_in_seconds: int | None = None,
    ) -> None:
        if not self._redis_available:
            return

        ttl = expires_in_seconds or self.get_remaining_ttl(token)
        if ttl <= 0:
            return

        key = self._token_key(token)
        await self._redis.setex(key, ttl, "1")

    async def is_blacklisted(self, token: str) -> bool:
        if not self._redis_available:
            return False

        key = self._token_key(token)
        return await self._redis.exists(key) > 0

    async def revoke_token(self, token: str) -> None:
        await self.blacklist_token(token)

    def create_access_token(
        self,
        subject: str,
        expires_delta: timedelta | None = None,
        additional_claims: dict[str, Any] | None = None,
    ) -> str:
        claims = {"type": "access"}
        if additional_claims:
            claims.update(additional_claims)
        return self.create_token(
            subject=subject,
            expires_delta=expires_delta,
            additional_claims=claims,
        )

    def create_refresh_token(
        self,
        subject: str,
        expires_delta: timedelta | None = None,
        additional_claims: dict[str, Any] | None = None,
    ) -> str:
        claims = {"type": "refresh"}
        if additional_claims:
            claims.update(additional_claims)
        return self.create_token(
            subject=subject,
            expires_delta=expires_delta or timedelta(days=30),
            additional_claims=claims,
        )
