"""
Classes API Endpoints
FastAPI routes for fitness class operations.
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
import logging

from app.models.class_models import ClassResponse, ClassStats
from app.services.class_service import ClassService
from app.utils.timezone_utils import validate_timezone
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


def get_class_service() -> ClassService:
    """Dependency to get class service instance"""
    return ClassService()


@router.get("/classes", response_model=List[ClassResponse])
async def get_classes(
    timezone: str = Query(
        default=settings.DEFAULT_TIMEZONE,
        description="Timezone for displaying class times"
    ),
    upcoming_only: bool = Query(
        default=True,
        description="Show only upcoming classes"
    ),
    instructor: Optional[str] = Query(
        default=None,
        description="Filter by instructor name"
    ),
    limit: int = Query(
        default=settings.DEFAULT_PAGE_SIZE,
        le=settings.MAX_PAGE_SIZE,
        description="Maximum number of classes to return"
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Number of classes to skip"
    ),
    class_service: ClassService = Depends(get_class_service)
):
    """
    Get fitness classes with optional filtering and timezone conversion
    """
    try:
        if not validate_timezone(timezone):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid timezone: {timezone}"
            )

        classes = class_service.get_classes(
            timezone=timezone,
            upcoming_only=upcoming_only,
            instructor=instructor,
            limit=limit,
            offset=offset
        )

        logger.info(
            f"Retrieved {len(classes)} classes for timezone {timezone}, "
            f"upcoming_only={upcoming_only}, instructor={instructor}"
        )

        return classes

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving classes: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error while retrieving classes"
        )


@router.get("/classes/{class_id}", response_model=ClassResponse)
async def get_class_by_id(
    class_id: int,
    timezone: str = Query(
        default=settings.DEFAULT_TIMEZONE,
        description="Timezone for displaying class time"
    ),
    class_service: ClassService = Depends(get_class_service)
):
    """
    Get a specific fitness class by ID
    """
    try:
        if not validate_timezone(timezone):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid timezone: {timezone}"
            )

        fitness_class = class_service.get_class_by_id(class_id, timezone)

        if not fitness_class:
            raise HTTPException(
                status_code=404,
                detail=f"Class with ID {class_id} not found"
            )

        logger.info(f"Retrieved class {class_id} for timezone {timezone}")
        return fitness_class

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving class {class_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error while retrieving class"
        )


@router.get("/classes/stats", response_model=ClassStats)
async def get_class_stats(
    class_service: ClassService = Depends(get_class_service)
):
    """
    Get statistics about fitness classes
    """
    try:
        stats = await class_service.get_class_stats()
        logger.info("Retrieved class statistics")
        return stats

    except Exception as e:
        logger.error(f"Error retrieving class stats: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error while retrieving class statistics"
        )


@router.get("/classes/instructors", response_model=List[str])
async def get_instructors(
    class_service: ClassService = Depends(get_class_service)
):
    """
    Get list of all instructors
    """
    try:
        instructors = await class_service.get_instructors()
        logger.info(f"Retrieved {len(instructors)} instructors")
        return instructors

    except Exception as e:
        logger.error(f"Error retrieving instructors: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error while retrieving instructors"
        )