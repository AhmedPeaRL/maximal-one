#!/usr/bin/env python3

import json
from pathlib import Path


PATH = Path(
    "artifacts/solar_periodicity_nuisance_audit.json"
)


def fail(message):
    raise SystemExit(f"❌ {message}")


def main():
    if not PATH.is_file():
        fail(
            "Solar periodicity nuisance audit is missing."
        )

    with PATH.open(encoding="utf-8") as f:
        data = json.load(f)

    if data.get("scientific_role") != "diagnostic_only":
        fail(
            "Solar nuisance audit must remain diagnostic-only."
        )

    if data.get("claim_support_eligible") is not False:
        fail(
            "Solar nuisance audit must not support the claim."
        )

    if data.get("confirmatory_use") is not False:
        fail(
            "Solar nuisance audit must not be confirmatory evidence."
        )

    policy = data.get(
        "interpretation_policy",
        {},
    )

    required = [
        "no_endpoint_optimization",
        "no_band_selection",
        "no_posthoc_claim",
        "nuisance_treatment_requires_preconfirmation_rule",
    ]

    for key in required:
        if policy.get(key) is not True:
            fail(
                f"Required epistemic policy missing: {key}"
            )

    harmonics = data.get(
        "harmonic_assessment",
        [],
    )

    if not harmonics:
        fail(
            "Harmonic assessment is missing."
        )

    if not any(
        item.get("inside_canonical_band") is True
        for item in harmonics
    ):
        fail(
            "Audit must explicitly assess whether "
            "solar harmonics enter the canonical band."
        )

    print(
        "✅ Solar periodicity nuisance audit "
        "is diagnostic-only and epistemically locked."
    )


if __name__ == "__main__":
    main()
