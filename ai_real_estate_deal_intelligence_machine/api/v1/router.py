from fastapi import APIRouter

from .routes import (
    health,
    deals,
    intelligence,
    recommendations,
    workflows,
    pipelines,
    intelligence_packages,
    investor_reports,
    deal_packages,
    buyer_matches,
    buyer_outreach,
    seller_outreach,
    seller_leads,

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


api_router.include_router(
    pipelines.router
)


api_router.include_router(
    intelligence_packages.router
)


api_router.include_router(
    investor_reports.router
)


api_router.include_router(
    deal_packages.router
)


api_router.include_router(
    buyer_matches.router
)


api_router.include_router(
    buyer_outreach.router
)
api_router.include_router(
    seller_outreach.router
)
api_router.include_router(
    seller_leads.router
)