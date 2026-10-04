from __future__ import annotations

import json
from pathlib import Path


PATH = Path("artifacts/null_calibration_audit.json")


def main() -> None:
    if not PATH.is_file():
        raise SystemExit(
            "❌ Missing null calibration audit artifact."
        )

    with PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if data.get("scientific_role") != "diagnostic_only":
        raise SystemExit(
            "❌ Null calibration must remain diagnostic_only."
        )

    if data.get("claim_support") is not False:
        raise SystemExit(
            "❌ Null calibration must never support claim promotion."
        )

    review = data.get("model_capacity_review", {})

    if review.get("review_triggered") is not True:
        raise SystemExit(
            "❌ Expected model-capacity review to remain triggered."
        )

    if review.get("boundary_fraction_threshold") != 0.50:
        raise SystemExit(
            "❌ Unexpected boundary-fraction threshold."
        )

    reasons = review.get("review_reasons", [])

    if len(reasons) < 1:
        raise SystemExit(
            "❌ Capacity review is triggered but no review reasons exist."
        )

    for result in data.get("results", []):
        if result.get("claim_support") is not False:
            raise SystemExit(
                "❌ Calibration result incorrectly supports claim promotion."
            )

    print(
        "✅ Null calibration remains diagnostic-only."
    )

    print(
        "🛑 Model-capacity review remains active."
    )

    print(
        f"Review reasons: {len(reasons)}"
    )

    print(
        "Claim promotion remains blocked."
    )


if __name__ == "__main__":
    main()
