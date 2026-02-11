from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import analysis, health
from config import settings
from app.utils.logger import app_logger

# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(analysis.router)

@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    app_logger.info(f"Starting {settings.API_TITLE} v{settings.API_VERSION}")
    app_logger.info(f"Debug mode: {settings.DEBUG}")
    app_logger.info(f"CORS origins: {settings.CORS_ORIGINS}")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    app_logger.info(f"Shutting down {settings.API_TITLE}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to CosmoChroma API",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
