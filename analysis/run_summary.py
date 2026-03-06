import json
import os
import time
import platform
import hashlib
import random

os.makedirs("artifacts", exist_ok=True)

data = {
    "timestamp": time.time(),
    "system": platform.system(),
    "python": platform.python_version(),
    "seed": random.randint(0, 10_000_000),
}

fingerprint = hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()

data["fingerprint"] = fingerprint

with open("artifacts/run_summary.json","w") as f:
    json.dump(data,f,indent=2)
