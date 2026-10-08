"""
Database Service Layer
Graceful dual-backend: SQLite (default zero-config) + Optional MySQL on port 3307.
Never blocks queue operations if database encounters an issue.
"""

import sqlite3
import logging
from typing import Dict, Any, List, Optional
from config import Config

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.mode = "SQLite"
        self.mysql_available = False
        self._test_and_select_backend()
        self.init_db()

    def _test_and_select_backend(self):
        """Attempts MySQL connection on port 3307 if credentials are provided."""
        if Config.DB_PASSWORD:
            try:
                import pymysql
                conn = pymysql.connect(
                    host=Config.DB_HOST,
                    port=Config.DB_PORT,
                    user=Config.DB_USER,
                    password=Config.DB_PASSWORD,
                    database=Config.DB_NAME,
                    connect_timeout=2
                )
                conn.close()
                self.mode = "MySQL"
                self.mysql_available = True
                logger.info(f"Connected to MySQL on port {Config.DB_PORT}")
                return
            except Exception as e:
                logger.warning(f"MySQL unavailable on port {Config.DB_PORT} ({e}). Falling back to SQLite.")
        
        self.mode = "SQLite"
        self.mysql_available = False

    def _get_connection(self):
        if self.mode == "MySQL":
            try:
                import pymysql
                return pymysql.connect(
                    host=Config.DB_HOST,
                    port=Config.DB_PORT,
                    user=Config.DB_USER,
                    password=Config.DB_PASSWORD,
                    database=Config.DB_NAME,
                    cursorclass=pymysql.cursors.DictCursor,
                    autocommit=True
                )
            except Exception as e:
                logger.error(f"MySQL error at runtime: {e}. Falling back to SQLite.")
                self.mode = "SQLite"
        
        # SQLite connection
        conn = sqlite3.connect(Config.SQLITE_DB_PATH, timeout=5)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Creates tables if they do not exist."""
        try:
            if self.mode == "MySQL":
                conn = self._get_connection()
                with conn.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS queue_sessions (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            session_uuid VARCHAR(64) UNIQUE NOT NULL,
                            capacity INT NOT NULL DEFAULT 5,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                        );
                    """)
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS operation_history (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            session_uuid VARCHAR(64),
                            operation VARCHAR(32) NOT NULL,
                            value VARCHAR(64),
                            front_index INT NOT NULL,
                            rear_index INT NOT NULL,
                            size INT NOT NULL,
                            capacity INT NOT NULL,
                            wrapped BOOLEAN DEFAULT 0,
                            message TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                    """)
                conn.close()
            else:
                conn = self._get_connection()
                with conn:
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS queue_sessions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            session_uuid VARCHAR(64) UNIQUE NOT NULL,
                            capacity INTEGER NOT NULL DEFAULT 5,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                    """)
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS operation_history (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            session_uuid VARCHAR(64),
                            operation VARCHAR(32) NOT NULL,
                            value VARCHAR(64),
                            front_index INTEGER NOT NULL,
                            rear_index INTEGER NOT NULL,
                            size INTEGER NOT NULL,
                            capacity INTEGER NOT NULL,
                            wrapped BOOLEAN DEFAULT 0,
                            message TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                    """)
                conn.close()
        except Exception as e:
            logger.error(f"Error initializing database: {e}")

    def log_operation(
        self,
        session_uuid: str,
        operation: str,
        value: Optional[Any],
        front: int,
        rear: int,
        size: int,
        capacity: int,
        wrapped: bool = False,
        message: str = ""
    ) -> bool:
        """Logs a circular queue operation safely."""
        try:
            val_str = str(value) if value is not None else None
            conn = self._get_connection()
            if self.mode == "MySQL":
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO operation_history 
                        (session_uuid, operation, value, front_index, rear_index, size, capacity, wrapped, message)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (session_uuid, operation, val_str, front, rear, size, capacity, int(wrapped), message))
                conn.close()
            else:
                with conn:
                    conn.execute("""
                        INSERT INTO operation_history 
                        (session_uuid, operation, value, front_index, rear_index, size, capacity, wrapped, message)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (session_uuid, operation, val_str, front, rear, size, capacity, int(wrapped), message))
                conn.close()
            return True
        except Exception as e:
            logger.warning(f"Could not log operation to database: {e}")
            return False

    def get_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetches recent operation history."""
        try:
            conn = self._get_connection()
            history = []
            if self.mode == "MySQL":
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id, operation, value, front_index, rear_index, size, capacity, wrapped, message, created_at
                        FROM operation_history
                        ORDER BY id DESC
                        LIMIT %s
                    """, (limit,))
                    history = cursor.fetchall()
                conn.close()
            else:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, operation, value, front_index, rear_index, size, capacity, wrapped, message, created_at
                    FROM operation_history
                    ORDER BY id DESC
                    LIMIT ?
                """, (limit,))
                rows = cursor.fetchall()
                for row in rows:
                    history.append({
                        "id": row["id"],
                        "operation": row["operation"],
                        "value": row["value"],
                        "front_index": row["front_index"],
                        "rear_index": row["rear_index"],
                        "size": row["size"],
                        "capacity": row["capacity"],
                        "wrapped": bool(row["wrapped"]),
                        "message": row["message"],
                        "created_at": str(row["created_at"])
                    })
                conn.close()
            return history
        except Exception as e:
            logger.error(f"Error fetching history: {e}")
            return []

    def clear_history(self) -> bool:
        """Clears all history logs."""
        try:
            conn = self._get_connection()
            if self.mode == "MySQL":
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM operation_history")
                conn.close()
            else:
                with conn:
                    conn.execute("DELETE FROM operation_history")
                conn.close()
            return True
        except Exception as e:
            logger.error(f"Error clearing history: {e}")
            return False

    def get_status(self) -> Dict[str, Any]:
        return {
            "mode": self.mode,
            "badge_text": f"{self.mode} Mode",
            "is_mysql": self.mode == "MySQL",
            "port": Config.DB_PORT if self.mode == "MySQL" else None
        }

db_service = DatabaseService()
