import json
import hashlib
import time
from datetime import datetime

INPUT = "artifacts/global_verdict.json"
OUTPUT = "public/artifact.json"

def load():
    try:
        with open(INPUT) as f:
            return json.load(f)
    except:
        return {"passed": False, "note": "no signal"}

def build_artifact(data):
    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "state": "stable" if data.get("passed") else "probing",
        "score": data.get("final_score", 0),
        "layer": data.get("layer", "unknown"),
    }

    raw = json.dumps(payload, sort_keys=True).encode()
    payload["signature"] = hashlib.sha256(raw).hexdigest()

    return payload

def save(obj):
    with open(OUTPUT, "w") as f:
        json.dump(obj, f, indent=2)

if __name__ == "__main__":
    data = load()
    artifact = build_artifact(data)
    save(artifact)
