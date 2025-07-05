"""
Logger Configuration
Sets up application-wide logging.
"""

import logging
from app.config import settings


def setup_logging() -> logging.Logger:
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format=settings.LOG_FORMAT
    )
    return logging.getLogger("fitness-api")