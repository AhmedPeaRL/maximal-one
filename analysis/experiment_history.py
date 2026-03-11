import json
import os
from datetime import datetime

REPORT_PATH = "artifacts/canonical_report.json"
HISTORY_PATH = "data/experiment_history.json"

def load_report():
    if not os.path.exists(REPORT_PATH):
        return None
    with open(REPORT_PATH) as f:
        return json.load(f)

def load_history():
    if not os.path.exists(HISTORY_PATH):
        return []
    with open(HISTORY_PATH) as f:
        return json.load(f)

def save_history(history):
    with open(HISTORY_PATH,"w") as f:
        json.dump(history,f,indent=2)

def main():

    report = load_report()
    if report is None:
        print("No canonical report found.")
        return

    history = load_history()

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "spectral_alpha": report.get("spectral_profile",{}).get("estimated_alpha"),
        "bootstrap_std": report.get("spectral_profile",{}).get("bootstrap_std"),
        "environment": report.get("_environment",{})
    }

    history.append(entry)

    save_history(history)

    print("Experiment history updated.")

if __name__ == "__main__":
    main()
