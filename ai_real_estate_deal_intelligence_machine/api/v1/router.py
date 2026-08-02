from fastapi import APIRouter

from .routes import (
    health,
    deals,
    intelligence,
    recommendations,
    workflows,
)


api_router = APIRouter(
    prefix="/api/v1"
)


api_router.include_router(
    health.router
)


api_router.include_router(
    deals.router
)


api_router.include_router(
    intelligence.router
)


api_router.include_router(
    recommendations.router
)


api_router.include_router(
    workflows.router
)