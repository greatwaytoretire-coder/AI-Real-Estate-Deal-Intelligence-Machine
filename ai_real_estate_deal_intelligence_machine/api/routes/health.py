from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
def health():
    return {
        "status": "operational",
        "system": "AI Real Estate Deal Intelligence Machine",
        "version": "1.0.0",
    }