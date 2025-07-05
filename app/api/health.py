"""
Health Check Endpoint
"""

from fastapi import APIRouter
from app.database import check_database_health

router = APIRouter()


@router.get("/health", tags=["Health"])
async def health_check():
    db_ok = check_database_health()
    return {
        "status": "ok" if db_ok else "degraded",
        "database": "healthy" if db_ok else "unhealthy"
    }