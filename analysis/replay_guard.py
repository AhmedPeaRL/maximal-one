import json
import os
import time
import hashlib

STORE = "data/replay_guard.json"
WINDOW = 60  # seconds

def load():
    if not os.path.exists(STORE):
        return {}
    with open(STORE) as f:
        return json.load(f)

def save(d):
    os.makedirs("data", exist_ok=True)
    with open(STORE, "w") as f:
        json.dump(d, f)

def fingerprint(payload):
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

def check(payload):
    db = load()
    now = time.time()
    fp = fingerprint(payload)

    # تنظيف القديم
    db = {k:v for k,v in db.items() if now - v < WINDOW}

    if fp in db:
        print("❌ Replay attack detected")
        return False

    db[fp] = now
    save(db)

    print("✅ Fresh witness accepted")
    return True
