import json
import sys
import math

REPORT_PATH = "artifacts/canonical_report.json"

def load_report():
    try:
        with open(REPORT_PATH) as f:
            return json.load(f)
    except Exception as e:
        print("❌ Failed to load report:", e)
        sys.exit(1)

def evaluate_claim(report):
    try:
        alpha = report["spectral_profile"]["estimated_alpha"]
        sigma = report["spectral_profile"]["bootstrap_std"]
    except:
        print("❌ Missing spectral fields")
        sys.exit(1)

    # === HARD SCIENTIFIC CLAIM ===
    # H0: alpha <= 0.5  (random / noise-like)
    # H1: alpha > 0.5   (structured / non-random)

    threshold = 0.5

    # Z-score style decision
    z = (alpha - threshold) / (sigma + 1e-9)

    if z > 2:
        return True, z
    elif z < -2:
        return False, z
    else:
        return None, z

def main():
    report = load_report()
    result, z = evaluate_claim(report)

    print("=== FALSIFIABILITY GATE ===")
    print("Z-score:", z)

    if result is True:
        print("✅ CLAIM SUPPORTED")
        sys.exit(0)

    elif result is False:
        print("❌ CLAIM REJECTED")
        sys.exit(1)

    else:
        print("⚠️ INCONCLUSIVE — SYSTEM NOT ALLOWED TO PASS")
        sys.exit(1)

if __name__ == "__main__":
    main()
