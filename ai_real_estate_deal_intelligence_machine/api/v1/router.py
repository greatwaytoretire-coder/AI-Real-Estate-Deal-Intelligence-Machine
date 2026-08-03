from fastapi import APIRouter

from .routes import (
    acquisition_deals,
    acquisition_offers,
    acquisition_workflows,
    buyer_matches,
    buyer_outreach,
    contracts,
    deal_packages,
    deals,
    health,
    intelligence,
    intelligence_packages,
    investor_reports,
    negotiations,
    pipelines,
    recommendations,
    seller_leads,
    seller_outreach,
    workflows,
    due_diligence,
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

api_router.include_router(
    acquisition_workflows.router
)

api_router.include_router(
    acquisition_deals.router
)

api_router.include_router(
    acquisition_offers.router
)

api_router.include_router(
    negotiations.router
)

api_router.include_router(
    contracts.router
)
api_router.include_router(
    due_diligence.router
)