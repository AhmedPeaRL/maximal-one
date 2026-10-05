#!/usr/bin/env python3

import json
from pathlib import Path


STRICT_CLAIM = Path("core-scientific/strict_claim.json")

REQUIRED_PROTOCOL = Path(
    "protocol/FUTURE_NULL_FREEZE_RULE.md"
)

def fail(message):
    raise SystemExit(f"❌ {message}")


def main():
    if not STRICT_CLAIM.is_file():
        fail("strict_claim.json is missing.")

    if not REQUIRED_PROTOCOL.is_file():
        fail("Future null-freeze protocol is missing.")

    with STRICT_CLAIM.open(encoding="utf-8") as f:
        claim = json.load(f)

    null = claim.get("stochastic_null_protocol", {})
    capacity = null.get("capacity_review_gate", {})
    review = null.get("model_capacity_review", {})

    if capacity.get(
        "current_primary_result_usable_for_claim_promotion"
    ) is not False:
        fail(
            "Current primary result must remain blocked until "
            "future null validation is completed."
        )

    if capacity.get(
        "fresh_null_validation_required_before_confirmatory_inference"
    ) is not True:
        fail(
            "Fresh null validation must be required before "
            "confirmatory inference."
        )

    if capacity.get(
        "historical_results_must_not_be_reused_as_confirmatory_evidence"
    ) is not True:
        fail(
            "Historical exploratory results must remain "
            "non-confirmatory."
        )

    if review.get("boundary_fraction_threshold") != 0.50:
        fail(
            "Unexpected capacity-review threshold."
        )

    if review.get("surrogate_boundary_fraction") is None:
        fail(
            "Current primary capacity result is missing."
        )

    if review.get("surrogate_boundary_fraction") >= review.get(
        "boundary_fraction_threshold"
    ):
        if review.get(
            "claim_promotion_blocked_until_review"
        ) is not True:
            fail(
                "Boundary saturation must block claim promotion."
            )

    if null.get(
        "preregistered_confirmation"
    ) is not False:
        fail(
            "Current exploratory null protocol must not "
            "be represented as preregistered confirmation."
        )

    print("✅ Confirmatory-readiness safety gate verified.")
    print("Claim promotion remains blocked until a fresh")
    print("prospectively frozen null protocol is validated.")


if __name__ == "__main__":
    main()
