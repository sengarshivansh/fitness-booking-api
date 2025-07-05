"""
Database Configuration and Management
SQLite database setup and connection handling for the Fitness Studio Booking API.
"""

import sqlite3
import logging
from contextlib import contextmanager
from typing import Generator

from app.config import settings, get_database_path

logger = logging.getLogger(__name__)


def init_database() -> None:
    """Initialize the SQLite database with required tables"""
    database_path = get_database_path()
    
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        
        # Create classes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                instructor TEXT NOT NULL,
                datetime_utc TEXT NOT NULL,
                total_slots INTEGER NOT NULL,
                available_slots INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create bookings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id TEXT PRIMARY KEY,
                class_id INTEGER NOT NULL,
                client_name TEXT NOT NULL,
                client_email TEXT NOT NULL,
                booking_time TEXT NOT NULL,
                status TEXT DEFAULT 'confirmed',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (class_id) REFERENCES classes (id)
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_classes_datetime 
            ON classes(datetime_utc)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_bookings_email 
            ON bookings(client_email)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_bookings_class_id 
            ON bookings(class_id)
        ''')
        
        conn.commit()
        conn.close()
        
        logger.info(f"Database initialized successfully at {database_path}")
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    """
    Context manager for database connections
    Ensures proper connection handling and cleanup
    """
    database_path = get_database_path()
    conn = sqlite3.connect(database_path)
    conn.row_factory = sqlite3.Row  # Enable dict-like access to rows
    
    try:
        yield conn
    except Exception as e:
        conn.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        conn.close()


def execute_query(query: str, params: tuple = ()) -> list:
    """
    Execute a SELECT query and return results
    
    Args:
        query: SQL query string
        params: Query parameters
        
    Returns:
        List of query results
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        raise


def execute_insert(query: str, params: tuple = ()) -> int:
    """
    Execute an INSERT query and return the last row ID
    
    Args:
        query: SQL query string
        params: Query parameters
        
    Returns:
        Last inserted row ID
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.execute(query, params)
            conn.commit()
            return cursor.lastrowid
    except Exception as e:
        logger.error(f"Error executing insert: {e}")
        raise


def execute_update(query: str, params: tuple = ()) -> int:
    """
    Execute an UPDATE query and return the number of affected rows
    
    Args:
        query: SQL query string
        params: Query parameters
        
    Returns:
        Number of affected rows
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.execute(query, params)
            conn.commit()
            return cursor.rowcount
    except Exception as e:
        logger.error(f"Error executing update: {e}")
        raise


def get_table_count(table_name: str) -> int:
    """
    Get the number of records in a table
    
    Args:
        table_name: Name of the table
        
    Returns:
        Number of records
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            result = cursor.fetchone()
            return result["count"] if result else 0
    except Exception as e:
        logger.error(f"Error getting table count: {e}")
        return 0


def check_database_health() -> bool:
    """
    Check if the database is accessible and has the required tables
    
    Returns:
        True if database is healthy, False otherwise
    """
    try:
        with get_db_connection() as conn:
            # Check if tables exist
            cursor = conn.execute('''
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name IN ('classes', 'bookings')
            ''')
            tables = cursor.fetchall()
            
            if len(tables) != 2:
                logger.warning("Database missing required tables")
                return False
                
            # Check if we can perform basic operations
            cursor.execute("SELECT COUNT(*) FROM classes")
            cursor.execute("SELECT COUNT(*) FROM bookings")
            
            return True
            
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False