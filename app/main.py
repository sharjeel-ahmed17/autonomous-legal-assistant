from fastapi import FastAPI

from app.api.routes import api_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.lifespan_exmple import lifespan

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

register_exception_handlers(app)
app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}