from fastapi import APIRouter

from app.api.v1 import auth, bets, health, leaderboard, matches, users
from app.api.v1.admin import router as admin_router

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(matches.router)
api_router.include_router(bets.router)
api_router.include_router(leaderboard.router)
api_router.include_router(users.router)
api_router.include_router(admin_router)
