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

    # =========================
    # HARD PHYSICAL REALITY
    # =========================

    # realistic fractal / spectral bounds
    if not (0.2 < alpha < 2.2):
        fail(f"Alpha physically impossible: {alpha}")

    # sigma must be tight
    if sigma > 0.3:
        fail(f"Sigma indicates noise domination: {sigma}")

    # derived sanity check (very important)
    if alpha * sigma > 0.5:
        fail(f"Unstable alpha-sigma coupling: {alpha * sigma}")

    print("✅ Physical layer PASSED")

if __name__ == "__main__":
    main()
