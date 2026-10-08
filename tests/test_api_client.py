import urllib.request
import json

def test_api():
    base = "http://127.0.0.1:5000"
    
    # 1. Health
    with urllib.request.urlopen(f"{base}/api/health") as r:
        health = json.loads(r.read())
        print("Health check:", health)
        assert health["status"] == "healthy"
    
    # 2. Reset / Create
    req = urllib.request.Request(
        f"{base}/api/queue/create",
        data=json.dumps({"capacity": 5}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as r:
        state = json.loads(r.read())
        print("Create Queue:", state["capacity"], "Size:", state["size"])
        assert state["capacity"] == 5 and state["size"] == 0
    
    # 3. Enqueue 10, 20
    for v in [10, 20]:
        req = urllib.request.Request(
            f"{base}/api/queue/enqueue",
            data=json.dumps({"value": v}).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as r:
            st = json.loads(r.read())
            print(f"Enqueued {v} -> front={st['front']}, rear={st['rear']}, size={st['size']}")
    
    # 4. Peek
    with urllib.request.urlopen(f"{base}/api/queue/peek") as r:
        pk = json.loads(r.read())
        print("Peek:", pk["operation_result"]["front_element"])
        assert pk["operation_result"]["front_element"] == 10
    
    # 5. Display
    with urllib.request.urlopen(f"{base}/api/queue/display") as r:
        disp = json.loads(r.read())
        print("Display logical order:", disp["operation_result"]["logical_order"])
        assert disp["operation_result"]["logical_order"] == [10, 20]
    
    # 6. Dequeue
    req = urllib.request.Request(
        f"{base}/api/queue/dequeue",
        data=b"{}",
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as r:
        dq = json.loads(r.read())
        print("Dequeued:", dq["operation_result"]["removed_value"], "New Front:", dq["front"])
        assert dq["operation_result"]["removed_value"] == 10
        assert dq["front"] == 1
    
    # 7. History
    with urllib.request.urlopen(f"{base}/api/history") as r:
        hist = json.loads(r.read())
        print("History count:", len(hist["history"]))
        assert len(hist["history"]) >= 3
    
    print("ALL API CHECKS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_api()
