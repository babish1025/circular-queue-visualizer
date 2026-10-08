"""
Circular Queue Visualizer - Flask Application
Academic Data Structures Web System
Authors: Babish P K, Bersha S K, Alisha, Jharna (2026)
"""

from flask import Flask, jsonify, request, render_template, send_from_directory
from queue_manager import queue_manager
from database import db_service
from config import Config
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config.from_object(Config)


# ==========================================
# PAGE & STATIC PWA ROUTES
# ==========================================

@app.route("/")
def index():
    """Serves the main single-screen visualizer interface."""
    return render_template("index.html")


@app.route("/manifest.json")
def manifest():
    """Serves the PWA Web App Manifest."""
    return send_from_directory("static", "manifest.json", mimetype="application/manifest+json")


@app.route("/service-worker.js")
def service_worker():
    """Serves the PWA Service Worker for offline static asset caching."""
    return send_from_directory("static", "service-worker.js", mimetype="application/javascript")


# ==========================================
# REST API ENDPOINTS
# ==========================================

@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint indicating backend & DB readiness."""
    db_status = db_service.get_status()
    return jsonify({
        "status": "healthy",
        "app": "Circular Queue Visualizer",
        "version": "1.0.0",
        "academic_year": "2026",
        "database": db_status
    })


@app.route("/api/queue/state", methods=["GET"])
def get_state():
    """Returns current state of circular queue."""
    state = queue_manager.get_state()
    return jsonify(state)


@app.route("/api/queue/create", methods=["POST"])
def create_queue():
    """Initializes queue with specified capacity."""
    data = request.get_json(silent=True) or {}
    capacity = data.get("capacity", 5)
    try:
        capacity = int(capacity)
        if capacity < 2 or capacity > 12:
            return jsonify({"success": False, "error": "Capacity must be between 2 and 12"}), 400
        result = queue_manager.create_queue(capacity)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/queue/enqueue", methods=["POST"])
def enqueue():
    """Enqueues a value into the circular queue."""
    data = request.get_json(silent=True) or {}
    value = data.get("value")
    if value is None or str(value).strip() == "":
        return jsonify({
            "success": False,
            "error": "EMPTY_VALUE",
            "message": "Please enter a valid value to enqueue."
        }), 400

    result = queue_manager.enqueue(value)
    # Return 200 even on overflow so the UI receives full state & educational breakdown
    status_code = 200 if result.get("success") else 400
    return jsonify(result), status_code


@app.route("/api/queue/dequeue", methods=["POST"])
def dequeue():
    """Dequeues front element from circular queue."""
    result = queue_manager.dequeue()
    status_code = 200 if result.get("success") else 400
    return jsonify(result), status_code


@app.route("/api/queue/peek", methods=["GET"])
def peek():
    """Peeks at front element without removal."""
    result = queue_manager.peek()
    status_code = 200 if result.get("success") else 400
    return jsonify(result), status_code


@app.route("/api/queue/display", methods=["GET"])
def display():
    """Retrieves logical FIFO order of elements."""
    result = queue_manager.display()
    return jsonify(result)


@app.route("/api/queue/clear", methods=["POST"])
def clear():
    """Clears all elements in current queue."""
    result = queue_manager.clear()
    return jsonify(result)


@app.route("/api/queue/reset", methods=["POST"])
def reset():
    """Resets queue to initial capacity (default 5)."""
    data = request.get_json(silent=True) or {}
    capacity = data.get("capacity")
    result = queue_manager.reset(capacity)
    return jsonify(result)


@app.route("/api/queue/demo-steps", methods=["GET"])
def demo_steps():
    """Returns the Professor Demo sequence steps."""
    steps = queue_manager.get_professor_demo_script()
    return jsonify({"success": True, "steps": steps})


@app.route("/api/history", methods=["GET"])
def history():
    """Returns persistent database operation history."""
    limit = request.args.get("limit", 50, type=int)
    history_records = db_service.get_history(limit=limit)
    return jsonify({
        "success": True,
        "database": db_service.get_status(),
        "history": history_records
    })


@app.route("/api/history/clear", methods=["POST"])
def clear_history():
    """Clears persistent database operation history."""
    success = db_service.clear_history()
    return jsonify({"success": success})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
