import json
import os
from datetime import datetime

LOG_DIR = "data/log_intelligence"
os.makedirs(LOG_DIR, exist_ok=True)

def extract_signal(log_file):
    try:
        with open(log_file) as f:
            data = json.load(f)
    except:
        return None

    signal = {
        "timestamp": datetime.utcnow().isoformat(),
        "alpha": data.get("spectral_profile", {}).get("estimated_alpha"),
        "std": data.get("spectral_profile", {}).get("bootstrap_std"),
    }

    return signal

def run():
    source = "artifacts/canonical_report.json"

    if not os.path.exists(source):
        return

    signal = extract_signal(source)
    if not signal:
        return

    out = os.path.join(LOG_DIR, f"signal_{int(datetime.utcnow().timestamp())}.json")

    with open(out, "w") as f:
        json.dump(signal, f)

if __name__ == "__main__":
    run()
