import json
import sys
from pathlib import Path

REPORT_PATH = Path("artifacts/canonical_report.json")
CLAIM_PATH = Path("core-scientific/strict_claim.json")

def run():
    print("=== FALSIFIABILITY GATE ===")

    if not REPORT_PATH.exists():
        print("❌ Canonical report missing")
        sys.exit(1)

    if not CLAIM_PATH.exists():
        print("❌ strict_claim.json missing")
        sys.exit(1)

    try:
        report = json.loads(
            REPORT_PATH.read_text(encoding="utf-8")
        )

        claim = json.loads(
            CLAIM_PATH.read_text(encoding="utf-8")
        )

        alpha = float(
            report["spectral_profile"]["estimated_alpha"]
        )

        sigma = float(
            report["spectral_profile"]["bootstrap_std"]
        )

        expected = claim["expected_result"]

        alpha_min, alpha_max = map(
            float,
            expected["alpha_range"]
        )

        max_sigma = float(
            expected["max_sigma"]
        )

    except Exception as exc:
        print(
            "❌ Invalid scientific configuration:",
            type(exc).__name__,
            str(exc)
        )
        sys.exit(1)

    print(f"alpha = {alpha}")
    print(f"sigma = {sigma}")
    print(
        f"canonical alpha range = "
        f"[{alpha_min}, {alpha_max}]"
    )
    print(f"canonical max sigma = {max_sigma}")

    reasons = []

    if not (alpha_min <= alpha <= alpha_max):
        reasons.append(
            "Alpha outside canonical strict-claim range"
        )

    if sigma > max_sigma:
        reasons.append(
            "Sigma exceeds canonical strict-claim bound"
        )

    if reasons:
        print("❌ FALSIFICATION CONDITION TRIGGERED")

        for reason in reasons:
            print("-", reason)

        sys.exit(1)

    print(
        "✅ No falsification condition triggered "
        "under the canonical strict-claim bounds."
    )

    print(
        "Important: this does NOT prove the model."
    )

    sys.exit(0)

if __name__ == "__main__":
    run()
