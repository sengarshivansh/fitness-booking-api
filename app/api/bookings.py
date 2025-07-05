"""
Bookings API Endpoints
FastAPI routes for class booking operations.
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
import logging

from app.models.booking_models import BookingRequest, BookingResponse
from app.services.booking_service import BookingService

logger = logging.getLogger(__name__)
router = APIRouter()


def get_booking_service() -> BookingService:
    return BookingService()


@router.post("/book", response_model=BookingResponse)
async def book_class(
    booking: BookingRequest,
    booking_service: BookingService = Depends(get_booking_service)
):
    try:
        return booking_service.create_booking(booking)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Booking error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/bookings", response_model=List[BookingResponse])
async def get_bookings_by_email(
    email: str = Query(..., description="Client email to filter bookings"),
    booking_service: BookingService = Depends(get_booking_service)
):
    try:
        return booking_service.get_bookings_by_email(email)
    except Exception as e:
        logger.error(f"Error fetching bookings: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")