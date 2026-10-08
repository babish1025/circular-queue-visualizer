# Circular Queue Mobile-First Visualizer

> **Academic Data Structures Interactive System — 2026**  
> Developed by: **Babish P K • Bersha S K • Alisha • Jharna**

An interactive, responsive, mobile-first learning application and visualization tool designed for students and professors to understand **Circular Queue** concepts, modulo arithmetic, pointer progression, boundary conditions (Overflow & Underflow), and the critical difference between the **Physical Array** and the **Logical FIFO Queue**.

---

## 📱 Mobile-First Experience
This application was engineered **Mobile-First**. Rather than shrinking a desktop website, the primary user interface is specifically optimized for touch screens, smartphones (Android & iOS), tablets, and modern desktop browsers:
- **One-Screen Control Center:** Fits the entire core Circular Queue workflow on standard mobile phone resolutions (such as **360 × 800**, **390 × 844**, **412 × 915**) without endless vertical scrolling.
- **Finger-Friendly Touch Targets:** All touch targets meet or exceed recommended accessibility standards (min 44px–48px).
- **Adaptive Visualizer:** Slots intelligently adapt dynamically to any capacity from 2 to 12.
- **High-Visibility Pointer Badges:** Sleek neon badges for `FRONT ↓`, `REAR ↑`, and combined `FRONT • REAR` pointers with animated movements.
- **PWA (Progressive Web App):** Installable to your mobile home screen (`manifest.json` + `service-worker.js`) with offline static caching.

---

## 🎯 Educational Objectives Covered
1. **FIFO (First-In, First-Out):** Elements are removed strictly in the order they arrived.
2. **FRONT & REAR Pointers:** `FRONT` tracks the head element, `REAR` tracks the tail element.
3. **Circular Modulo Arithmetic:**
   $$\text{Next REAR} = (\text{REAR} + 1) \pmod{\text{Capacity}}$$
   $$\text{Next FRONT} = (\text{FRONT} + 1) \pmod{\text{Capacity}}$$
4. **Boundary Checks:**
   - **Queue Overflow:** $\text{Size} == \text{Capacity}$ or $(\text{REAR} + 1) \pmod{\text{Capacity}} == \text{FRONT}$
   - **Queue Underflow:** $\text{Size} == 0$ or $\text{FRONT} == -1$
5. **Circular Wrap-Around:** Immediate animated notification when pointer loops back from `Capacity - 1` to `0`.
6. **Physical Array vs. Logical FIFO:** Demonstrates how physical array memory slots diverge from logical FIFO ordering during wrap-around.
7. **Learning Mode (`💡 LEARN`):** Expandable bottom drawer displaying real-time step-by-step mathematical calculations for every operation.
8. **Professor Demo Mode (`🎓 DEMO`):** Automated step-through sequence demonstrating capacity 5, overflow prevention, dequeueing, wrapping rear, and the resulting physical vs logical queue state.

---

## 🏗️ Architecture

```text
Circular Queue Visualizer/
│
├── app.py                  # Flask Application & REST API Endpoints
├── config.py               # Dual Database Configuration (SQLite & MySQL 3307)
├── queue_engine.py         # Pure Python In-Memory CircularQueue Class (Engine)
├── queue_manager.py        # Business Logic & Demo Script Orchestration
├── database.py             # Dual Database Access Layer (SQLite/PyMySQL)
├── run.py                  # Primary Entrypoint with LAN IP Detection
├── requirements.txt        # Python Dependencies
│
├── templates/
│   └── index.html          # Mobile-First HTML5 Shell
│
├── static/
│   ├── css/
│   │   └── style.css       # Mobile-First Cyber Academic Dark Design System
│   ├── js/
│   │   └── app.js          # Touch UI Logic, State Sync, PWA, Demo Runner
│   ├── icons/
│   │   └── icon.svg        # Scalable PWA Vector Icon
│   ├── manifest.json       # Web App Manifest (Standalone Mode)
│   └── service-worker.js   # Offline Static Resource Cache
│
├── database/
│   └── schema.sql          # SQL Schema for Session and Operation Logging
│
└── tests/
    └── test_queue.py       # Comprehensive Unit Tests (13 Edge Cases)
```

---

## ⚡ Installation & Setup

### Prerequisites
- Python 3.10+ (Tested on Python 3.12)
- Pip

### 1. Clone or Open Project Directory
```bash
cd "c:\Users\BABISH\.gemini\antigravity-ide\scratch\Circular Queue"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Application

Start the application with one command:
```bash
python run.py
```
*(You can also use `python app.py`)*

The terminal will automatically detect your LAN IP address and display:
```text
========================================================================
       ↻ CIRCULAR QUEUE MOBILE-FIRST VISUALIZER
       Academic Data Structures Interactive System — 2026
========================================================================
  Developed by:
  Babish P K  •  Bersha S K  •  Alisha  •  Jharna

  Database Backend : ● SQLite Mode
  
  [ACCESS LINKS]
  • Desktop (Localhost) : http://127.0.0.1:5000
  • Mobile Phone (LAN)  : http://<YOUR-COMPUTER-IP>:5000
========================================================================
```

---

## 📱 Mobile Phone Access on Local Wi-Fi
To use the application directly on your Android phone, iPhone, or iPad:
1. Make sure your phone is connected to the **same Wi-Fi network** as your computer.
2. If your IP address changes, run:
   ```bash
   ipconfig
   ```
   and find your **IPv4 Address** (e.g., `192.168.1.50`).
3. On your phone's browser (Chrome, Safari, Firefox), navigate to:
   ```text
   http://<YOUR-COMPUTER-IP>:5000
   ```
4. **Install as PWA:**
   - On Android Chrome: Tap the 3 dots menu $\to$ **"Add to Home screen"** or **"Install app"**.
   - On iOS Safari: Tap the Share button $\to$ **"Add to Home Screen"**.

---

## 🗄️ Database: SQLite & Optional MySQL

### Default: Zero-Config SQLite
The visualizer runs out of the box using **SQLite** (`instance/circular_queue.db`). No configuration or database service installation is required.

### Optional: MySQL on Port 3307
If you wish to log operations to MySQL on port 3307, set the following environment variables:
```bash
set DB_HOST=localhost
set DB_PORT=3307
set DB_NAME=circular_queue_db
set DB_USER=root
set DB_PASSWORD=your_mysql_password
```
- **Graceful Fallback:** If MySQL is not running or credentials are unavailable, the application **automatically falls back to SQLite** without throwing errors or breaking queue operations.
- The UI status pill will honestly show `● SQLite Mode` or `● MySQL Mode`.
- The in-memory Circular Queue remains the source of truth for high-performance operations.

---

## 🌐 REST API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Service health status and active database engine |
| `GET` | `/api/queue/state` | Full state snapshot (slots, pointers, sizes, arrays) |
| `POST` | `/api/queue/create` | Re-initializes queue with custom capacity (`{"capacity": 5}`) |
| `POST` | `/api/queue/enqueue` | Enqueues a value (`{"value": 50}`) |
| `POST` | `/api/queue/dequeue` | Dequeues the front element |
| `GET` | `/api/queue/peek` | Returns front element without removing |
| `GET` | `/api/queue/display` | Returns logical FIFO array |
| `POST` | `/api/queue/clear` | Empties all slots |
| `POST` | `/api/queue/reset` | Resets to default capacity 5 |
| `GET` | `/api/queue/demo-steps` | Returns Professor Demo sequence script |
| `GET` | `/api/history` | Fetches persistent database operation history |
| `POST` | `/api/history/clear` | Clears historical operation logs |

---

## 🧪 Testing

Run the automated test suite to verify all mathematical conditions and edge cases:
```bash
python -m unittest tests/test_queue.py
```

### Verified Test Cases:
1. `test_01_empty_queue`: Initial state ($front = -1, rear = -1, size = 0$).
2. `test_02_single_enqueue`: First insertion advances front and rear to 0.
3. `test_03_multiple_enqueue`: Monotonic rear progression.
4. `test_04_full_queue`: Full capacity detection.
5. `test_05_overflow`: Rejection with `QueueOverflowError`.
6. `test_06_dequeue`: Front pointer progression and value retrieval.
7. `test_07_underflow`: Rejection with `QueueUnderflowError`.
8. `test_08_peek`: Non-destructive front inspection.
9. `test_09_clear`: Slot resetting.
10. `test_10_reset`: Dynamic capacity changes.
11. `test_11_wrap_around_and_physical_vs_logical`: The core test:
    - Capacity = 5
    - Enqueue: 10, 20, 30, 40, 50
    - Dequeue: 10, 20
    - Enqueue: 60, 70
    - Expected Physical: `[60, 70, 30, 40, 50]`
    - Expected Logical: `[30, 40, 50, 60, 70]`
    - Pointers: $FRONT = 2$, $REAR = 1$, $Size = 5$.
12. `test_12_empty_after_full_dequeues`: Pointer reset to -1 upon reaching 0 elements.
13. `test_13_state_structure`: Slot tagging and pointer metadata verification.

---

## 👥 Project Team

**Circular Queue Visualizer**  
Academic Data Structures Project — 2026

- **Babish P K**
- **Bersha S K**
- **Alisha**
- **Jharna**
