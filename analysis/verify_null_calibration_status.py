from __future__ import annotations

import json
from pathlib import Path


CALIBRATION_REVIEW_IS_DIAGNOSTIC_ONLY = True
PRIMARY_NULL_CAPACITY_AUDIT_REQUIRED = True

PATH = Path(
    "artifacts/null_calibration_audit.json"
)


def main() -> None:
    if not PATH.is_file():
        raise SystemExit(
            "❌ Missing null calibration audit artifact."
        )

    with PATH.open(
        "r",
        encoding="utf-8",
    ) as f:
        data = json.load(f)

    if data.get(
        "scientific_role"
    ) != "diagnostic_only":
        raise SystemExit(
            "❌ Null calibration must remain diagnostic_only."
        )

    if data.get(
        "claim_support"
    ) is not False:
        raise SystemExit(
            "❌ Null calibration must never support claim promotion."
        )

    review = data.get(
        "model_capacity_review",
        {},
    )

    if review.get(
        "scientific_role"
    ) != "diagnostic_only":
        raise SystemExit(
            "❌ Model-capacity review must remain diagnostic_only."
        )

    if review.get(
        "claim_support"
    ) is not False:
        raise SystemExit(
            "❌ Model-capacity review must never support claim promotion."
        )

    if review.get(
        "boundary_fraction_threshold"
    ) != 0.50:
        raise SystemExit(
            "❌ Unexpected boundary-fraction threshold."
        )

    review_triggered = review.get(
        "review_triggered"
    )

    if review_triggered not in (
        True,
        False,
    ):
        raise SystemExit(
            "❌ review_triggered must be explicitly boolean."
        )

    reasons = review.get(
        "review_reasons",
        [],
    )

    if not isinstance(
        reasons,
        list,
    ):
        raise SystemExit(
            "❌ review_reasons must be a list."
        )

    if review_triggered and not reasons:
        raise SystemExit(
            "❌ Triggered review requires review reasons."
        )

    if not review_triggered and reasons:
        raise SystemExit(
            "❌ Non-triggered review cannot contain reasons."
        )

    for result in data.get(
        "results",
        [],
    ):
        if result.get(
            "claim_support"
        ) is not False:
            raise SystemExit(
                "❌ Calibration result incorrectly "
                "supports claim promotion."
            )

    print(
        "✅ Calibration result is diagnostic-only."
    )

    print(
        "ℹ️ Passing AR(1)/AR(2) calibration does not "
        "establish adequacy of the primary sunspot "
        "stochastic null."
    )

    print(
        "ℹ️ Primary-null capacity audit remains required."
    )

    if review_triggered:
        print(
            "⚠️ Model-capacity review is triggered "
            "for the declared calibration cases."
        )
    else:
        print(
            "✅ Model-capacity review is not triggered "
            "for the declared calibration cases."
        )

    print(
        f"Review reasons: {len(reasons)}"
    )

    print(
        "Claim promotion remains blocked."
    )


if __name__ == "__main__":
    main()
