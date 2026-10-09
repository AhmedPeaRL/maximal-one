#!/usr/bin/env python3

import json
from pathlib import Path


STRICT_CLAIM = Path("core-scientific/strict_claim.json")

REQUIRED_PROTOCOL = Path(
    "protocol/FUTURE_NULL_FREEZE_RULE.md"
)

READINESS_PATH = Path(
    "protocol/NULL_CONFIRMATORY_READINESS_V1.json"
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

    if not READINESS_PATH.is_file():
        fail(
            "Null confirmatory readiness file is missing."
        )

    with READINESS_PATH.open(encoding="utf-8") as f:
        readiness = json.load(f)

    if readiness.get("protocol") != (
        "NULL_CONFIRMATORY_READINESS_V1"
    ):
        fail(
            "Unexpected null confirmatory readiness protocol."
        )

    readiness_status = readiness.get("status")
    if readiness_status not in ("NOT_READY", "READY"):
        fail(
            "Readiness status must be explicitly NOT_READY or READY."
        )

    current = readiness.get("current_observed_state", {})
    decision = readiness.get("decision", {})

    boundary_fraction = current.get("boundary_fraction")
    boundary_threshold = current.get("boundary_fraction_threshold")

    if not isinstance(boundary_fraction, (int, float)):
        fail("Readiness boundary fraction must be numeric.")

    if not isinstance(boundary_threshold, (int, float)):
        fail("Readiness boundary threshold must be numeric.")

    if boundary_threshold != 0.50:
        fail(
            "Unexpected readiness boundary threshold; "
            "a threshold change requires fresh validation."
        )

    if readiness_status == "NOT_READY":
        if decision.get("confirmatory_inference_available") is not False:
            fail(
                "NOT_READY must prohibit confirmatory inference."
            )

        if decision.get("claim_promotion_allowed") is not False:
            fail(
                "NOT_READY must prohibit claim promotion."
            )

        if current.get("confirmatory_null_frozen") is not False:
            fail(
                "NOT_READY requires the confirmatory null to remain unfrozen."
            )

        if current.get("fresh_validation_required") is not True:
            fail(
                "NOT_READY requires fresh validation."
            )

        if boundary_fraction >= boundary_threshold:
            if current.get("capacity_review_required") is not True:
                fail(
                    "Boundary saturation requires capacity review."
                )

    else:
        if decision.get("confirmatory_inference_available") is not True:
            fail(
                "READY requires explicit confirmatory-inference readiness."
            )

        if decision.get("claim_promotion_allowed") is not False:
            fail(
                "Readiness file cannot grant claim-promotion authority."
            )

        if current.get("confirmatory_null_frozen") is not True:
            fail(
                "READY requires an explicitly frozen confirmatory null."
            )

        if boundary_fraction >= boundary_threshold:
            fail(
                "READY is inconsistent with unresolved boundary saturation."
            )

    print(
        "Null readiness protocol:",
        readiness_status,
    )
    print(
        "Null readiness grants claim-promotion authority: False"
    )
    
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
