from fastapi import APIRouter
from app.schemas.response_models import HealthResponse
from config import settings

router = APIRouter(
    prefix="/api",
    tags=["health"]
)

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify API is running
    
    Returns API status and version information
    """
    return HealthResponse(
        status="ok",
        version=settings.API_VERSION,
        message="API is running and ready to process requests"
    )
