import json
import hashlib
import time
import os

RESPONSES_FILE = "data/challenge_responses.json"
ANCHOR_FILE = "public/challenge_anchor.json"

def anchor():
    if not os.path.exists(RESPONSES_FILE):
        return

    with open(RESPONSES_FILE) as f:
        data = json.load(f)

    raw = json.dumps(data, sort_keys=True)

    anchor = {
        "timestamp": time.time(),
        "hash": hashlib.sha256(raw.encode()).hexdigest(),
        "count": len(data)
    }

    os.makedirs("public", exist_ok=True)

    with open(ANCHOR_FILE, "w") as f:
        json.dump(anchor, f, indent=2)

if __name__ == "__main__":
    anchor()
