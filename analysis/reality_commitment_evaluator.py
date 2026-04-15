import json
import time
import os

INPUT_PATH = "data/reality_commitments.json"
REPORT_PATH = "data/reality_commitment_results.json"

def evaluate():
    if not os.path.exists(INPUT_PATH):
        print("No commitments found")
        return

    with open(INPUT_PATH, "r") as f:
        commitments = json.load(f)

    results = []

    for c in commitments:
        if time.time() < c["timestamp"] + c["evaluation_after_seconds"]:
            continue

        BREACH_LOG = "data/reality_breach_log.json"

        if os.path.exists(BREACH_LOG):
            with open(BREACH_LOG, "r") as f:
                logs = json.load(f)
                actual_value = logs[-1]["evaluation"]["breach_score"]
        else:
            actual_value = 0

        success = abs(actual_value - c["predicted_value"]) <= c["tolerance"]

        results.append({
            "id": c["id"],
            "predicted": c["predicted_value"],
            "actual": actual_value,
            "success": success
        })

    with open(REPORT_PATH, "w") as f:
        json.dump(results, f, indent=2)

    print("Evaluation complete")

if __name__ == "__main__":
    evaluate()
