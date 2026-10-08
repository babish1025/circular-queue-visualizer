import urllib.request
import json

base = "http://127.0.0.1:5000"

def post(url, payload):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read()), None
    except urllib.error.HTTPError as e:
        return json.loads(e.read()), e.code

def get(url):
    with urllib.request.urlopen(url) as r:
        return json.loads(r.read())

print("=== CIRCULAR QUEUE - FULL WRAP-AROUND SCENARIO TEST ===")

# Reset
post(base + "/api/queue/create", {"capacity": 5})

# Enqueue 10..50
for v in [10, 20, 30, 40, 50]:
    post(base + "/api/queue/enqueue", {"value": v})
print("Enqueued: 10, 20, 30, 40, 50 (FULL)")

# Overflow attempt
data, code = post(base + "/api/queue/enqueue", {"value": 60})
print("Overflow (60) status:", data.get("error"), "HTTP:", code or "200")
assert data.get("error") == "OVERFLOW"

# Dequeue 10 and 20
for _ in range(2):
    data, _ = post(base + "/api/queue/dequeue", {})
    print("Dequeued:", data["operation_result"]["removed_value"])

# Enqueue 60 (wrap-around expected at REAR)
data, _ = post(base + "/api/queue/enqueue", {"value": 60})
print("Enqueued 60: REAR=", data["rear"], "| Wrapped=", data["operation_result"].get("wrapped"))
assert data["operation_result"].get("wrapped") == True

# Enqueue 70
data, _ = post(base + "/api/queue/enqueue", {"value": 70})
print("Enqueued 70: REAR=", data["rear"])

# Final state
state = get(base + "/api/queue/state")
print()
print("--- FINAL VERIFIED STATE ---")
print("Physical Array:", state["physical_array"])
print("Logical Queue: ", state["logical_queue"])
print("FRONT:", state["front"], "| REAR:", state["rear"], "| SIZE:", state["size"])

assert state["physical_array"] == [60, 70, 30, 40, 50]
assert state["logical_queue"] == [30, 40, 50, 60, 70]
assert state["front"] == 2
assert state["rear"] == 1
assert state["size"] == 5
assert state["is_full"] == True

# Test PEEK
pk = get(base + "/api/queue/peek")
print("Peek:", pk["operation_result"]["front_element"])
assert pk["operation_result"]["front_element"] == 30

# Test DISPLAY
dp = get(base + "/api/queue/display")
print("Display:", dp["operation_result"]["logical_order"])
assert dp["operation_result"]["logical_order"] == [30, 40, 50, 60, 70]

# Test CLEAR
post(base + "/api/queue/clear", {})
state = get(base + "/api/queue/state")
assert state["is_empty"] == True
assert state["front"] == -1
assert state["rear"] == -1
print("Clear: PASSED")

# Test RESET
post(base + "/api/queue/reset", {"capacity": 3})
state = get(base + "/api/queue/state")
assert state["capacity"] == 3
print("Reset to capacity 3: PASSED")

print()
print("=== ALL FUNCTIONAL TESTS PASSED! ===")
