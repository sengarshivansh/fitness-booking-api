"""
Timezone Utilities
Handles timezone conversion and validation.
"""

from datetime import datetime
import pytz


def convert_utc_to_local(utc_str: str, timezone: str) -> str:
    """Convert UTC ISO string to local time string"""
    utc_dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
    local_tz = pytz.timezone(timezone)
    local_dt = utc_dt.astimezone(local_tz)
    return local_dt.strftime("%Y-%m-%d %H:%M:%S")


def validate_timezone(tz: str) -> bool:
    """Check if a timezone string is valid"""
    return tz in pytz.all_timezones