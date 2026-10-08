-- Circular Queue Visualizer Database Schema
-- Compatible with SQLite and MySQL (port 3307)
-- Academic Year: 2026

CREATE TABLE IF NOT EXISTS queue_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_uuid VARCHAR(64) UNIQUE NOT NULL,
    capacity INTEGER NOT NULL DEFAULT 5,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

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

CREATE TABLE IF NOT EXISTS saved_demos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(128) NOT NULL,
    description TEXT,
    steps_json TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
