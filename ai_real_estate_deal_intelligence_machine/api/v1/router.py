from fastapi import APIRouter

from .routes import (
    acquisition_deals,
    acquisition_offers,
    acquisition_workflows,
    buyer_matches,
    buyer_outreach,
    contracts,
    closings,
    deal_packages,
    deals,
    due_diligence,
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
    asset_management,
    portfolio,
    portfolio_optimization,
    tenant_management,
    maintenance,
    lease_management,
    inspection_management,
    rent_collection, 
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

api_router.include_router(
    closings.router
)
api_router.include_router(
    asset_management.router
)
api_router.include_router(
    portfolio.router
)
api_router.include_router(
    portfolio_optimization.router
)
api_router.include_router(
    tenant_management.router
)
api_router.include_router(
    maintenance.router
)
api_router.include_router(
    lease_management.router,
    prefix="/lease-management",
    tags=["Lease Management"],
)
api_router.include_router(
    inspection_management.router,
    prefix="/inspection-management",
    tags=["Inspection Management"],
)
api_router.include_router(
    rent_collection.router,
    prefix="/rent-collection",
    tags=["Rent Collection"],
) 