from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.config import get_settings
from app.core.i18n import get_locale_from_request, get_translator
from app.core.jwt import decode_access_token, get_access_token_from_request
from app.database import SessionLocal
from app.services.auth import get_user_by_id
from app.web.router import web_router

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield


app = FastAPI(
    title=settings.app_name,
    description="REST API for the 2026 World Cup betting pool. Web UI routes are separate from `/api/v1/`.",
    version="1.0.0",
    debug=settings.debug,
    lifespan=lifespan,
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(web_router)
app.include_router(api_router, prefix="/api/v1")


@app.middleware("http")
async def locale_middleware(request: Request, call_next):
    locale = get_locale_from_request(request)
    request.state.locale = locale
    request.state._ = get_translator(locale)
    response = await call_next(request)
    return response


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    request.state.user = None
    token = get_access_token_from_request(request, settings)
    if token:
        user_id = decode_access_token(token, settings)
        if user_id is not None:
            db = SessionLocal()
            try:
                user = get_user_by_id(db, user_id)
                if user is not None and user.is_active:
                    request.state.user = user
            finally:
                db.close()
    response = await call_next(request)
    return response
