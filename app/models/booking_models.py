"""
Booking-related Pydantic Models
Data models for fitness class booking operations.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator

from app.config import settings


class BookingBase(BaseModel):
    """Base booking model with common fields"""
    client_name: str = Field(..., min_length=2, max_length=100, description="Client full name")
    client_email: EmailStr = Field(..., description="Client email address")
    
    @validator('client_name',allow_reuse=True)
    def validate_client_name(cls, v):
        """Validate client name is not empty after stripping"""
        if not v.strip():
            raise ValueError('Client name cannot be empty')
        return v.strip()


class BookingRequest(BookingBase):
    """Model for booking request"""
    class_id: int = Field(..., ge=1, description="ID of the class to book")
    timezone: str = Field(
        default=settings.DEFAULT_TIMEZONE,
        description="Client's timezone for datetime display"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "class_id": 1,
                "client_name": "John Doe",
                "client_email": "john.doe@example.com",
                "timezone": "Asia/Kolkata"
            }
        }


class BookingResponse(BookingBase):
    """Model for booking response"""
    id: str = Field(..., description="Unique booking ID")
    class_id: int = Field(..., description="Class ID")
    class_name: str = Field(..., description="Class name")
    instructor: str = Field(..., description="Instructor name")
    class_datetime_local: str = Field(..., description="Class datetime in local timezone")
    timezone: str = Field(..., description="Timezone used for datetime display")
    booking_time: str = Field(..., description="Booking timestamp in local timezone")
    status: str = Field(default="confirmed", description="Booking status")
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "class_id": 1,
                "class_name": "Yoga Basics",
                "instructor": "Priya Sharma",
                "client_name": "John Doe",
                "client_email": "john.doe@example.com",
                "class_datetime_local": "2025-07-10 07:00:00",
                "timezone": "Asia/Kolkata",
                "booking_time": "2025-07-06 14:30:00",
                "status": "confirmed"
            }
        }


class BookingUpdate(BaseModel):
    """Model for updating booking information"""
    client_name: Optional[str] = Field(None, min_length=2, max_length=100)
    status: Optional[str] = Field(None, regex="^(confirmed|cancelled|pending)$")
    
    @validator('client_name')
    def validate_client_name(cls, v):
        """Validate client name is not empty after stripping"""
        if v is not None and not v.strip():
            raise ValueError('Client name cannot be empty')
        return v.strip() if v else v


class BookingSummary(BaseModel):
    """Lightweight booking summary model"""
    id: str
    class_name: str
    class_datetime_local: str
    status: str


class BookingStats(BaseModel):
    """Model for booking statistics"""
    total_bookings: int = Field(..., description="Total number of bookings")
    confirmed_bookings: int = Field(..., description="Number of confirmed bookings")
    cancelled_bookings: int = Field(..., description="Number of cancelled bookings")
    unique_clients: int = Field(..., description="Number of unique clients")
    most_popular_class: Optional[str] = Field(None, description="Most popular class name")
    
    class Config:
        schema_extra = {
            "example": {
                "total_bookings": 150,
                "confirmed_bookings": 135,
                "cancelled_bookings": 15,
                "unique_clients": 75,
                "most_popular_class": "Yoga Basics"
            }
        }


class BookingFilter(BaseModel):
    """Model for filtering bookings"""
    email: Optional[EmailStr] = Field(None, description="Filter by client email")
    class_id: Optional[int] = Field(None, ge=1, description="Filter by class ID")
    status: Optional[str] = Field(None, regex="^(confirmed|cancelled|pending)$")
    date_from: Optional[str] = Field(None, description="Filter from date (YYYY-MM-DD)")
    date_to: Optional[str] = Field(None, description="Filter to date (YYYY-MM-DD)")
    
    @validator('date_from', 'date_to')
    def validate_dates(cls, v):
        """Validate date format"""
        if v is not None:
            try:
                datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                raise ValueError('Date must be in YYYY-MM-DD format')
        return v