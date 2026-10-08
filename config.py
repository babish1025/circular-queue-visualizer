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

    # MySQL configuration — Railway instance
    DB_HOST = os.environ.get("DB_HOST", "mysql.railway.internal")
    DB_PORT = int(os.environ.get("DB_PORT", "3306"))
    DB_NAME = os.environ.get("DB_NAME", "railway")
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "XgKmcpqrIemiXCxuqdzsiKoAfgeAsgdw")
    DB_URL = os.environ.get("DATABASE_URL", "mysql://root:XgKmcpqrIemiXCxuqdzsiKoAfgeAsgdw@mysql.railway.internal:3306/railway")
    
    # Server network settings
    HOST = "0.0.0.0"
    PORT = int(os.environ.get("PORT", 5000))
