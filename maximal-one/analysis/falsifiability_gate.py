import json
import sys

REPORT_PATH = "artifacts/canonical_report.json"

def run():
    print("=== FALSIFIABILITY GATE ===")

    try:
        with open(REPORT_PATH) as f:
            report = json.load(f)
    except Exception as e:
        print("❌ Cannot load report:", str(e))
        sys.exit(1)

    try:
        alpha = report["spectral_profile"]["estimated_alpha"]
        sigma = report["spectral_profile"]["bootstrap_std"]
    except KeyError:
        print("❌ Invalid report structure")
        sys.exit(1)

    # -----------------------------
    # HARD SCIENTIFIC BOUNDARIES
    # -----------------------------
    ALPHA_MIN = 0.45
    ALPHA_MAX = 0.60
    MAX_SIGMA = 0.05

    print(f"alpha = {alpha}")
    print(f"sigma = {sigma}")

    # -----------------------------
    # FALSIFICATION CONDITIONS
    # -----------------------------
    falsified = False
    reasons = []

    if not (ALPHA_MIN <= alpha <= ALPHA_MAX):
        falsified = True
        reasons.append("Alpha out of expected range")

    if sigma > MAX_SIGMA:
        falsified = True
        reasons.append("Sigma too high (instability)")

    # -----------------------------
    # DECISION
    # -----------------------------
    if falsified:
        print("❌ MODEL FALSIFIED")
        print("Reasons:")
        for r in reasons:
            print("-", r)

        # HARD FAIL → BREAK PIPELINE
        sys.exit(1)
    else:
        print("✅ Model NOT falsified (still valid under current evidence)")
        sys.exit(0)


if __name__ == "__main__":
    run()
