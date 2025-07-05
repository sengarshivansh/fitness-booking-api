"""
Class Service
Business logic for managing fitness classes.
"""

import uuid
from datetime import datetime,UTC
from typing import List, Optional

from app.models.class_models import ClassResponse, ClassStats
from app.database import execute_query
from app.utils.timezone_utils import convert_utc_to_local
from app.config import get_database_path


class ClassService:
    def get_classes(
        self,
        timezone: str,
        upcoming_only: bool = True,
        instructor: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[ClassResponse]:
        query = "SELECT * FROM classes"
        filters = []
        params = []

        if upcoming_only:
            filters.append("datetime_utc > ?")
            params.append(datetime.now(UTC).isoformat())

        if instructor:
            filters.append("instructor = ?")
            params.append(instructor)

        if filters:
            query += " WHERE " + " AND ".join(filters)

        query += " ORDER BY datetime_utc ASC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        rows = execute_query(query, tuple(params))

        return [
            ClassResponse(
                id=row["id"],
                name=row["name"],
                instructor=row["instructor"],
                datetime_local=convert_utc_to_local(row["datetime_utc"], timezone),
                timezone=timezone,
                available_slots=row["available_slots"],
                total_slots=row["total_slots"]
            )
            for row in rows
        ]

    def get_class_by_id(self, class_id: int, timezone: str) -> Optional[ClassResponse]:
        query = "SELECT * FROM classes WHERE id = ?"
        rows = execute_query(query, (class_id,))
        if not rows:
            return None

        row = rows[0]
        return ClassResponse(
            id=row["id"],
            name=row["name"],
            instructor=row["instructor"],
            datetime_local=convert_utc_to_local(row["datetime_utc"], timezone),
            timezone=timezone,
            available_slots=row["available_slots"],
            total_slots=row["total_slots"]
        )

    def get_class_stats(self) -> ClassStats:
        total_classes = execute_query("SELECT COUNT(*) as count FROM classes")[0]["count"]
        upcoming_classes = execute_query(
            "SELECT COUNT(*) as count FROM classes WHERE datetime_utc > ?",
            (datetime.utcnow().isoformat(),)
        )[0]["count"]
        total_bookings = execute_query("SELECT COUNT(*) as count FROM bookings")[0]["count"]
        popular = execute_query("""
            SELECT instructor, COUNT(*) as count
            FROM classes
            GROUP BY instructor
            ORDER BY count DESC
            LIMIT 1
        """)
        popular_instructor = popular[0]["instructor"] if popular else None

        return ClassStats(
            total_classes=total_classes,
            upcoming_classes=upcoming_classes,
            total_bookings=total_bookings,
            popular_instructor=popular_instructor
        )

    def get_instructors(self) -> List[str]:
        rows = execute_query("SELECT DISTINCT instructor FROM classes ORDER BY instructor ASC")
        return [row["instructor"] for row in rows]