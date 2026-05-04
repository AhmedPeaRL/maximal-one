import json
import hashlib
import time
import os

def generate():
    payload = {
        "timestamp": time.time(),
        "repo": os.getenv("GH_REPO", "unknown"),
        "run_id": os.getenv("GITHUB_RUN_ID", "local"),
    }

    raw = json.dumps(payload, sort_keys=True)
    fingerprint = hashlib.sha256(raw.encode()).hexdigest()

    output = {
        "payload": payload,
        "fingerprint": fingerprint
    }

    os.makedirs("artifacts", exist_ok=True)

    with open("artifacts/external_witness.json", "w") as f:
        json.dump(output, f, indent=2)

    print("✅ External witness generated:", fingerprint[:12])

if __name__ == "__main__":
    generate()
