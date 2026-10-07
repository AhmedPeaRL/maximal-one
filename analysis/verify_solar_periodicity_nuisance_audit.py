import json
from pathlib import Path


PATH = Path(
    "artifacts/solar_periodicity_nuisance_audit.json"
)


def fail(message):
    raise SystemExit(
        f"❌ {message}"
    )


def main():
    if not PATH.is_file():
        fail(
            "Solar periodicity nuisance audit is missing."
        )

    with PATH.open(
        encoding="utf-8"
    ) as f:
        data = json.load(f)

    if data.get(
        "scientific_role"
    ) != "diagnostic_only":
        fail(
            "Solar nuisance audit must remain "
            "diagnostic-only."
        )

    if data.get(
        "claim_support_eligible"
    ) is not False:
        fail(
            "Solar nuisance audit must not "
            "support the claim."
        )

    if data.get(
        "confirmatory_use"
    ) is not False:
        fail(
            "Solar nuisance audit must not "
            "be confirmatory evidence."
        )

    if data.get(
        "loader"
    ) != (
        "analysis.load_real_datasets.load_series"
    ):
        fail(
            "Solar nuisance audit must use "
            "the canonical repository loader."
        )

    policy = data.get(
        "interpretation_policy",
        {},
    )

    required_true = [
        "no_endpoint_optimization",
        "no_band_selection",
        "no_posthoc_claim",
        "nuisance_treatment_requires_preconfirmation_rule",
        "current_result_does_not_support_or_falsify_claim",
        "loader_must_match_canonical_repository_loader",
    ]

    for key in required_true:
        if policy.get(key) is not True:
            fail(
                f"Required epistemic policy missing: {key}"
            )

    if data.get(
        "sample_count",
        0,
    ) < 512:
        fail(
            "Solar nuisance audit sample count "
            "is below estimator minimum."
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
        item.get(
            "inside_canonical_band"
        ) is True
        for item in harmonics
    ):
        fail(
            "Audit must explicitly assess "
            "solar harmonics entering the "
            "canonical band."
        )

    print(
        "✅ Solar periodicity nuisance audit "
        "is diagnostic-only and epistemically locked."
    )


if __name__ == "__main__":
    main()
