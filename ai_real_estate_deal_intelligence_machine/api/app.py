from fastapi import FastAPI

from .v1.router import api_router


app = FastAPI(
    title="AI Real Estate Deal Intelligence Machine",
    version="1.0.0",
)


app.include_router(
    api_router
)


@app.get("/")
def root():
    return {
        "application": "AI Real Estate Deal Intelligence Machine",
        "status": "running",
        "version": "1.0.0",
    }