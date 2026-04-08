import json
import hashlib
from datetime import datetime

def generate_pre_witness():
    payload = {
        "phase": "pre-run",
        "timestamp": datetime.utcnow().isoformat(),
        "intent": "anticipation",
        "status": "initiated"
    }

    raw = json.dumps(payload, sort_keys=True)
    payload["hash"] = hashlib.sha256(raw.encode()).hexdigest()

    return payload

if __name__ == "__main__":
    w = generate_pre_witness()
    print(json.dumps(w, indent=2))
