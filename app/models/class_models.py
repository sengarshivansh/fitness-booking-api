"""
Class-related Pydantic Models
Data models for fitness class operations.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


class ClassBase(BaseModel):
    """Base class model with common fields"""
    name: str = Field(..., min_length=2, max_length=100, description="Class name")
    instructor: str = Field(..., min_length=2, max_length=100, description="Instructor name")
    total_slots: int = Field(..., ge=1, le=100, description="Total available slots")
    
    @validator('name', 'instructor')
    def validate_text_fields(cls, v):
        """Validate text fields are not empty after stripping"""
        if not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()


class ClassCreate(ClassBase):
    """Model for creating a new class"""
    datetime_utc: str = Field(..., description="Class datetime in UTC ISO format")
    
    @validator('datetime_utc')
    def validate_datetime(cls, v):
        """Validate datetime format and ensure it's in the future"""
        try:
            dt = datetime.fromisoformat(v.replace('Z', '+00:00'))
            if dt <= datetime.now():
                raise ValueError('Class datetime must be in the future')
            return v
        except ValueError as e:
            raise ValueError(f'Invalid datetime format: {e}')


class ClassUpdate(BaseModel):
    """Model for updating a class"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    instructor: Optional[str] = Field(None, min_length=2, max_length=100)
    datetime_utc: Optional[str] = None
    total_slots: Optional[int] = Field(None, ge=1, le=100)
    
    @validator('name', 'instructor')
    def validate_text_fields(cls, v):
        """Validate text fields are not empty after stripping"""
        if v is not None and not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip() if v else v


class ClassResponse(BaseModel):
    """Model for class response with timezone conversion"""
    id: int = Field(..., description="Class ID")
    name: str = Field(..., description="Class name")
    instructor: str = Field(..., description="Instructor name")
    datetime_local: str = Field(..., description="Class datetime in local timezone")
    timezone: str = Field(..., description="Timezone used for datetime display")
    available_slots: int = Field(..., ge=0, description="Available slots")
    total_slots: int = Field(..., ge=1, description="Total slots")
    
    class Config:
        """Pydantic configuration"""
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Yoga Basics",
                "instructor": "Priya Sharma",
                "datetime_local": "2025-07-10 07:00:00",
                "timezone": "Asia/Kolkata",
                "available_slots": 18,
                "total_slots": 20
            }
        }


class ClassSummary(BaseModel):
    """Lightweight class summary model"""
    id: int
    name: str
    instructor: str
    available_slots: int
    total_slots: int


class ClassStats(BaseModel):
    """Model for class statistics"""
    total_classes: int = Field(..., description="Total number of classes")
    upcoming_classes: int = Field(..., description="Number of upcoming classes")
    total_bookings: int = Field(..., description="Total number of bookings")
    popular_instructor: Optional[str] = Field(None, description="Most popular instructor")
    
    class Config:
        schema_extra = {
            "example": {
                "total_classes": 25,
                "upcoming_classes": 15,
                "total_bookings": 120,
                "popular_instructor": "Priya Sharma"
            }
        }