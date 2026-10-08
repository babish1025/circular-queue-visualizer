"""
Configuration Module for Circular Queue Visualizer
Supports SQLite (zero-config default) and optional MySQL on port 3307.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "academic-circular-queue-2026-secret-key")
    DEBUG = os.environ.get("FLASK_DEBUG", "True").lower() in ("1", "true")
    
    # SQLite default path
    INSTANCE_DIR = BASE_DIR / "instance"
    INSTANCE_DIR.mkdir(exist_ok=True)
    SQLITE_DB_PATH = str(INSTANCE_DIR / "circular_queue.db")

    # Optional MySQL configuration (Port 3307 as specified)
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = int(os.environ.get("DB_PORT", "3307"))
    DB_NAME = os.environ.get("DB_NAME", "circular_queue_db")
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")  # Do NOT hardcode password
    
    # Server network settings
    HOST = "0.0.0.0"
    PORT = int(os.environ.get("PORT", 5000))
