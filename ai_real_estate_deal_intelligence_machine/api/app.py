from fastapi import FastAPI

from ai_real_estate_deal_intelligence_machine.api.v1.router import (
    api_router,
)


app = FastAPI(
    title="AI Real Estate Deal Intelligence Machine",
    version="1.0.0",
)


app.include_router(
    api_router
)