"""
Booking Service
Business logic for managing class bookings.
"""

import uuid
from datetime import datetime
from typing import List

from app.models.booking_models import BookingRequest, BookingResponse
from app.database import execute_query, execute_insert
from app.utils.timezone_utils import convert_utc_to_local


class BookingService:
    def create_booking(self, booking: BookingRequest) -> BookingResponse:
        # Check class availability
        class_row = execute_query("SELECT * FROM classes WHERE id = ?", (booking.class_id,))
        if not class_row:
            raise ValueError("Class not found")

        class_data = class_row[0]
        if class_data["available_slots"] <= 0:
            raise ValueError("No available slots")

        # Create booking
        booking_id = str(uuid.uuid4())
        booking_time = datetime.utcnow().isoformat()

        execute_insert(
            """
            INSERT INTO bookings (id, class_id, client_name, client_email, booking_time)
            VALUES (?, ?, ?, ?, ?)
            """,
            (booking_id, booking.class_id, booking.client_name, booking.client_email, booking_time)
        )

        # Update available slots
        execute_insert(
            "UPDATE classes SET available_slots = available_slots - 1 WHERE id = ?",
            (booking.class_id,)
        )

        return BookingResponse(
            id=booking_id,
            class_id=booking.class_id,
            class_name=class_data["name"],
            instructor=class_data["instructor"],
            client_name=booking.client_name,
            client_email=booking.client_email,
            class_datetime_local=convert_utc_to_local(class_data["datetime_utc"], booking.timezone),
            timezone=booking.timezone,
            booking_time=convert_utc_to_local(booking_time, booking.timezone),
            status="confirmed"
        )

    def get_bookings_by_email(self, email: str) -> List[BookingResponse]:
        query = """
        SELECT b.*, c.name as class_name, c.instructor, c.datetime_utc
        FROM bookings b
        JOIN classes c ON b.class_id = c.id
        WHERE b.client_email = ?
        ORDER BY b.booking_time DESC
        """
        rows = execute_query(query, (email,))
        return [
            BookingResponse(
                id=row["id"],
                class_id=row["class_id"],
                class_name=row["class_name"],
                instructor=row["instructor"],
                client_name=row["client_name"],
                client_email=row["client_email"],
                class_datetime_local=convert_utc_to_local(row["datetime_utc"], "Asia/Kolkata"),
                timezone="Asia/Kolkata",
                booking_time=convert_utc_to_local(row["booking_time"], "Asia/Kolkata"),
                status=row["status"]
            )
            for row in rows
        ]