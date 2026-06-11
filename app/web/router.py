from fastapi import APIRouter

from app.web import auth, leaderboard, matches, pages, profile
from app.web.admin import router as admin_router

web_router = APIRouter(include_in_schema=False)
web_router.include_router(pages.router)
web_router.include_router(auth.router)
web_router.include_router(matches.router)
web_router.include_router(leaderboard.router)
web_router.include_router(profile.router)
web_router.include_router(admin_router)
