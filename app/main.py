"""
Fitness Studio Booking API - Main Application
FastAPI application with comprehensive booking system for fitness classes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import init_database
from app.api.classes import router as classes_router
from app.api.bookings import router as bookings_router
from app.api.health import router as health_router
from app.utils.logger import setup_logging
from scripts.seed_data import seed_sample_data

# Setup logging
logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("🚀 Starting Fitness Studio Booking API...")
    init_database()
    seed_sample_data()
    logger.info("✅ Database initialized and seeded successfully")
    yield
    # Shutdown
    logger.info("👋 Shutting down Fitness Studio Booking API...")

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(classes_router, prefix="/api/v1", tags=["Classes"])
app.include_router(bookings_router, prefix="/api/v1", tags=["Bookings"])
app.include_router(health_router, tags=["Health"])

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Fitness Studio Booking API",
        "version": settings.APP_VERSION,
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "endpoints": {
            "GET /api/v1/classes": "List all upcoming fitness classes",
            "POST /api/v1/book": "Book a fitness class",
            "GET /api/v1/bookings": "Get bookings by email",
            "GET /health": "Health check endpoint"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )