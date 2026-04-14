import json
import os
import hashlib
import time

STORE = "data/replay_guard.json"
WINDOW = 60  # seconds

if not os.path.exists("payload.json"):
    print("No payload")
    exit(0)

with open("payload.json") as f:
    data = json.load(f)

if data.get("_empty"):
    exit(0)

nonce = data.get("nonce")
timestamp = data.get("timestamp")

if not nonce or not timestamp:
    print("Missing replay fields")
    exit(1)

now = int(time.time() * 1000)

if abs(now - timestamp) > WINDOW * 1000:
    print("Replay window exceeded")
    exit(1)

# Load store
if os.path.exists(STORE):
    with open(STORE) as f:
        store = json.load(f)
else:
    store = {}

# Clean old
store = {
    k: v for k, v in store.items()
    if now - v < WINDOW * 1000
}

if nonce in store:
    print("Replay detected")
    exit(1)

store[nonce] = now

os.makedirs("data", exist_ok=True)

with open(STORE, "w") as f:
    json.dump(store, f, indent=2)

print("Replay guard passed")
