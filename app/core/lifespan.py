from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.database import create_db_and_tables, engine
from app.core.logging import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting %s...", settings.APP_NAME)

    if settings.APP_ENV == "development":
        logger.info("Creating database tables...")
        await create_db_and_tables()
        logger.info("Database tables ready.")

    yield

    logger.info("Shutting down %s...", settings.APP_NAME)

    await engine.dispose()
    logger.info("Database engine disposed.")