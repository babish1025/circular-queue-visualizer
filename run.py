"""
Circular Queue Visualizer - Main Runner
Runs Flask on 0.0.0.0:5000 with LAN detection for mobile phone testing.
"""

import socket
import sys
from app import app
from config import Config
from database import db_service


if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def get_local_ip() -> str:
    """Attempts to find the primary local IPv4 address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connecting to a public address (doesn't send actual packet)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        try:
            ip = socket.gethostbyname(socket.gethostname())
        except Exception:
            ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def print_banner():
    local_ip = get_local_ip()
    port = Config.PORT
    db_status = db_service.get_status()

    banner = f"""
========================================================================
       [CIRCULAR QUEUE MOBILE-FIRST VISUALIZER]
       Academic Data Structures Interactive System -- 2026
========================================================================
  Developed by:
  Babish P K  *  Bersha S K  *  Alisha  *  Jharna

  Database Backend : {db_status['badge_text']}
  
  [ACCESS LINKS]
  * Desktop (Localhost) : http://127.0.0.1:{port}
  * Mobile Phone (LAN)  : http://{local_ip}:{port}
  
  [MOBILE TESTING INSTRUCTIONS]
  1. Connect your phone to the SAME Wi-Fi network as this PC.
  2. Open Chrome/Safari on your phone and browse to:
     http://{local_ip}:{port}
  3. If your IP changed, check 'ipconfig' in command prompt for IPv4.
  4. (Optional) In Chrome on Android, tap 'Add to Home screen' for PWA!
========================================================================
Starting Flask server on 0.0.0.0:{port}...
"""
    try:
        print(banner)
    except UnicodeEncodeError:
        print(f"Server starting on http://127.0.0.1:{port} and http://{local_ip}:{port}")


if __name__ == "__main__":
    print_banner()
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)

