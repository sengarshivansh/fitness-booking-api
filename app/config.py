"""
Application Configuration
Centralized configuration management for the Fitness Studio Booking API.
"""

import os
from typing import List
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # App Information
    APP_NAME: str = "Fitness Studio Booking API"
    APP_DESCRIPTION: str = "A comprehensive booking system for fitness classes with timezone support"
    APP_VERSION: str = "1.0.0"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # Database Configuration
    DATABASE_FILE: str = "fitness_studio.db"
    
    # Timezone Configuration
    DEFAULT_TIMEZONE: str = "Asia/Kolkata"
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 50
    MAX_PAGE_SIZE: int = 100
    
    # Business Rules
    MAX_BOOKINGS_PER_USER: int = 5
    BOOKING_ADVANCE_DAYS: int = 30
    
    class Config:
        """Pydantic configuration"""
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


def get_database_path() -> str:
    """Get the full database path"""
    if os.path.isabs(settings.DATABASE_FILE):
        return settings.DATABASE_FILE
    return os.path.join(os.getcwd(), settings.DATABASE_FILE)


def is_production() -> bool:
    """Check if running in production environment"""
    return not settings.DEBUG


def get_allowed_timezones() -> List[str]:
    """Get list of commonly used timezones"""
    return [
        "UTC",
        "Asia/Kolkata",
        "America/New_York",
        "Europe/London",
        "Asia/Tokyo",
        "Australia/Sydney",
        "America/Los_Angeles",
        "Europe/Paris",
        "Asia/Dubai",
        "America/Chicago"
    ]