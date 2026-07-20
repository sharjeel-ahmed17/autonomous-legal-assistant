from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.logging import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Autonomous Legal Assistant...")

    # Initialize application resources here.
    #
    # Examples:
    # - Database
    # - Redis
    # - Qdrant
    # - MCP Clients
    # - LLM Clients
    # - Background Tasks

    yield

    logger.info("Shutting down Autonomous Legal Assistant...")

    # Cleanup resources here.
    #
    # Examples:
    # - Close Redis
    # - Close Database
    # - Close HTTP Clients
    # - Stop Background Tasks