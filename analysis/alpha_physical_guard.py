import json
import sys

REPORT_PATH = "artifacts/canonical_report.json"

def fail(msg):
    print("❌", msg)
    sys.exit(1)

def main():
    with open(REPORT_PATH) as f:
        r = json.load(f)

    alpha = r["spectral_profile"]["estimated_alpha"]
    sigma = r["spectral_profile"]["bootstrap_std"]

    # Physical plausibility bounds (critical fix)
    if not (0.0 < alpha < 3.0):
        fail(f"Alpha out of physical bounds: {alpha}")

    # Stability constraint
    if sigma > 0.5:
        fail(f"Sigma too high (unstable signal): {sigma}")

    print("✅ Alpha physically plausible")

if __name__ == "__main__":
    main()
