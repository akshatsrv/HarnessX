from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.cases import router as cases_router
from app.api.v1.claims import router as claims_router
from app.api.v1.documents import router as documents_router
from app.api.v1.health import router as health_router
from app.api.v1.investigations import router as investigations_router
from app.core.config import settings
from app.core.errors import ClaimGuardException, claimguard_exception_handler
from app.core.logging import logger, setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Initializing ClaimGuard AI Application...")
    yield
    logger.info("Shutting down ClaimGuard AI Application.")


app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered insurance claims investigation and fraud-risk decision support platform.",
    version="0.1.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(ClaimGuardException, claimguard_exception_handler)

# Routers
app.include_router(health_router, prefix="/api/v1")
app.include_router(claims_router, prefix="/api/v1")
app.include_router(documents_router, prefix="/api/v1")
app.include_router(investigations_router, prefix="/api/v1")
app.include_router(cases_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": "0.1.0",
        "docs_url": "/docs",
        "api_v1_prefix": "/api/v1"
    }
