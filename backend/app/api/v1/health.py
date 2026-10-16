from fastapi import APIRouter
from app.core.config import settings
from app.schemas.responses import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        environment=settings.APP_ENV,
        services={
            "api": "operational",
            "bigquery": "connected",
            "document_ai": "ready",
            "vertex_ai": "ready",
            "firestore": "ready"
        }
    )
