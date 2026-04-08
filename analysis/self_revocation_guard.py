import json
import os
import sys

THRESHOLD = 0.6

def load_latest_report():
    path = "artifacts/canonical_report.json"
    if not os.path.exists(path):
        return None

    with open(path) as f:
        return json.load(f)

def compute_confidence(report):
    try:
        alpha = report["spectral_profile"]["estimated_alpha"]
        std = report["spectral_profile"]["bootstrap_std"]

        # simple confidence heuristic
        score = max(0, min(1, 1 - (std / (abs(alpha) + 1e-6))))
        return score
    except:
        return 0

def main():
    report = load_latest_report()

    if not report:
        print("No report found → neutral state")
        return

    confidence = compute_confidence(report)

    print(f"[SELF-REVOCATION] confidence = {confidence:.4f}")

    if confidence < THRESHOLD:
        print("⚠️ Low confidence → triggering soft revocation")
        sys.exit(1)
    else:
        print("✅ Confidence stable")

if __name__ == "__main__":
    main()
