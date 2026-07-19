from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = Field(...)
    APP_VERSION: str = Field(...)
    APP_ENV: str = Field(...)
    DEBUG: bool = Field(...)

    HOST: str = Field(...)
    PORT: int = Field(...)

    SECRET_KEY: str = Field(...)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(...)

    DATABASE_URL: str = Field(...)

    REDIS_URL: str = Field(...)

    QDRANT_URL: str = Field(...)
    QDRANT_API_KEY: str = Field(default="")
    QDRANT_COLLECTION: str = Field(...)

    OPENAI_API_KEY: str = Field(default="")
    GROQ_API_KEY: str = Field(default="")
    COHERE_API_KEY: str = Field(default="")

    CHAT_MODEL: str = Field(...)
    EMBEDDING_MODEL: str = Field(...)

    LANGSMITH_TRACING: bool = Field(False)
    LANGSMITH_API_KEY: str = Field(default="")
    LANGSMITH_PROJECT: str = Field(default="")
    LANGSMITH_ENDPOINT: str = Field(default="")

    UPLOAD_DIR: str = Field(...)
    MAX_UPLOAD_SIZE_MB: int = Field(...)

    OCR_PROVIDER: str = Field(...)
    OCR_MODEL: str = Field(...)

    TOP_K: int = Field(...)
    CHUNK_SIZE: int = Field(...)
    CHUNK_OVERLAP: int = Field(...)

    LOG_LEVEL: str = Field(...)

    BACKEND_CORS_ORIGINS: str = Field(...)

    MCP_ENABLED: bool = Field(True)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

if __name__ == "__main__":
    pass
    # from rich import print
    # print(settings.APP_NAME)
    # print(settings.DATABASE_URL)
