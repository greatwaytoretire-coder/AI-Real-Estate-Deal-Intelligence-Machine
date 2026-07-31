from fastapi import APIRouter


router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("")
def health_check():
    return {
        "status": "operational",
        "system": "AI Real Estate Deal Intelligence Machine",
        "version": "1.0.0",
        "api": "v1",
    }