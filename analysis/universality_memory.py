import json
import os
from datetime import datetime

HISTORY = "data/universality_history.json"
CURRENT = "artifacts/universality_gate.json"

os.makedirs("data", exist_ok=True)

if not os.path.exists(HISTORY):
    with open(HISTORY, "w") as f:
        json.dump([], f)

with open(HISTORY) as f:
    hist = json.load(f)

if os.path.exists(CURRENT):
    with open(CURRENT) as f:
        current = json.load(f)

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "score": current.get("score", 0),
        "passed": current.get("passed", False)
    }

    hist.append(entry)

    # keep last 200 فقط
    hist = hist[-200:]

    with open(HISTORY, "w") as f:
        json.dump(hist, f, indent=2)

    print("Memory updated.")
else:
    print("No current result.")
