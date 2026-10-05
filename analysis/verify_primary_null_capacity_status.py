from __future__ import annotations

import json
from pathlib import Path


PATH = Path("artifacts/primary_null_capacity_audit.json")


def main() -> None:
    if not PATH.is_file():
        raise SystemExit(
            "❌ Missing primary-null capacity audit artifact."
        )

    with PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if data.get("scientific_role") != "diagnostic_only":
        raise SystemExit(
            "❌ Primary-null capacity audit must be diagnostic_only."
        )

    if data.get("claim_support") is not False:
        raise SystemExit(
            "❌ Primary-null capacity audit must never support claim promotion."
        )

    if data.get("preregistered_confirmation") is not False:
        raise SystemExit(
            "❌ Capacity audit must not be treated as preregistered confirmation."
        )

    if data.get("loader") != (
        "analysis.load_real_datasets.load_series"
    ):
        raise SystemExit(
            "❌ Primary-null capacity audit must use the canonical dataset loader."
        )

    max_order = data.get("max_order")
    hold_back = data.get("comparison_hold_back")

    if hold_back != max_order:
        raise SystemExit(
            "❌ Comparison hold-back must equal maximum candidate order."
        )

    threshold = data.get("boundary_fraction_threshold")

    if threshold != 0.50:
        raise SystemExit(
            "❌ Unexpected boundary-fraction threshold."
        )

    review = data.get("review_triggered")

    if review not in (True, False):
        raise SystemExit(
            "❌ review_triggered must be boolean."
        )

    reasons = data.get("review_reasons", [])

    if not isinstance(reasons, list):
        raise SystemExit(
            "❌ review_reasons must be a list."
        )

    if review and not reasons:
        raise SystemExit(
            "❌ Triggered review requires explicit reasons."
        )

    if not review and reasons:
        raise SystemExit(
            "❌ Non-triggered review cannot contain reasons."
        )

    valid_refits = data.get("valid_surrogate_refits", 0)

    if valid_refits < 200:
        raise SystemExit(
            "❌ Fewer than 200 valid surrogate refits are available."
        )

    boundary_fraction = data.get(
        "surrogate_boundary_fraction"
    )

    if not isinstance(boundary_fraction, (int, float)):
        raise SystemExit(
            "❌ Missing numeric surrogate boundary fraction."
        )

    print("✅ Primary-null capacity audit contract verified.")
    print(
        "Observed selected order:",
        data.get("observed_selected_order"),
    )
    print(
        "Maximum declared order:",
        max_order,
    )
    print(
        "Valid surrogate refits:",
        valid_refits,
    )
    print(
        "Surrogate boundary fraction:",
        boundary_fraction,
    )
    print(
        "Review triggered:",
        review,
    )
    print(
        "Claim promotion remains blocked."
    )


if __name__ == "__main__":
    main()
