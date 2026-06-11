from fastapi import APIRouter

from app.web import auth, pages

web_router = APIRouter()
web_router.include_router(pages.router)
web_router.include_router(auth.router)
