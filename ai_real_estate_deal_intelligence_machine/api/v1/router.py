from fastapi import APIRouter

from .routes import health, deals


api_router = APIRouter(
    prefix="/api/v1"
)


api_router.include_router(
    health.router
)

api_router.include_router(
    deals.router
)