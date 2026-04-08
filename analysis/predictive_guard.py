import json
import os
from collections import Counter

LOG_DIR = "data/external"

def load_logs():
    logs = []
    if not os.path.exists(LOG_DIR):
        return logs
    
    for f in os.listdir(LOG_DIR):
        if f.endswith(".json"):
            try:
                with open(os.path.join(LOG_DIR, f)) as file:
                    logs.append(json.load(file))
            except:
                continue
    return logs

def detect_patterns(logs):
    sizes = [len(json.dumps(l)) for l in logs if isinstance(l, dict)]
    
    if not sizes:
        return {"status": "no-data"}
    
    avg = sum(sizes) / len(sizes)
    
    anomalies = [s for s in sizes if s > avg * 2]
    
    return {
        "avg_size": avg,
        "anomaly_count": len(anomalies),
        "risk": "high" if len(anomalies) > len(sizes) * 0.2 else "normal"
    }

def main():
    logs = load_logs()
    result = detect_patterns(logs)
    
    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/predictive_guard.json", "w") as f:
        json.dump(result, f)

    print("Predictive guard:", result)

if __name__ == "__main__":
    main()
