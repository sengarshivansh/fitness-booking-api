"""
Seed Data Script
Populates the database with sample fitness classes.
"""

from datetime import datetime, timedelta
from app.database import execute_insert, get_table_count


def seed_sample_data():
    if get_table_count("classes") > 0:
        return  # Already seeded

    now = datetime.utcnow()
    classes = [
        ("Yoga Basics", "Priya Sharma", now + timedelta(days=1), 20),
        ("HIIT Blast", "Rahul Mehta", now + timedelta(days=2), 15),
        ("Zumba Fun", "Anjali Rao", now + timedelta(days=3), 25),
    ]

    for name, instructor, dt, slots in classes:
        execute_insert(
            """
            INSERT INTO classes (name, instructor, datetime_utc, total_slots, available_slots, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name, instructor, dt.isoformat(), slots, slots, now.isoformat())
        )