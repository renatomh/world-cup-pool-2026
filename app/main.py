from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.config import get_settings
from app.core.i18n import get_locale_from_request, get_translator
from app.web.router import web_router

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
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
