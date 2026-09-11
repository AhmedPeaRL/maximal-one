from __future__ import annotations
import json
import math
from pathlib import Path

REPORT_PATH = Path("artifacts/canonical_report.json")
CLAIM_PATH = Path("core-scientific/strict_claim.json")

def finite(value):
    return isinstance(value, (int, float)) and math.isfinite(float(value))

def require(condition, message):
    if not condition:
        raise SystemExit(
            "❌ INTERNAL SCIENTIFIC CONSISTENCY FAILURE: "
            f"{message}"
        )

def finite_float(value, name):
    require(
        finite(value),
        f"{name} is missing or non-finite: {value}",
    )
    return float(value)

def main():
    require(
        REPORT_PATH.exists(),
        f"missing report: {REPORT_PATH}",
    )

    require(
        CLAIM_PATH.exists(),
        f"missing claim specification: {CLAIM_PATH}",
    )

    with REPORT_PATH.open(
        "r",
        encoding="utf-8",
    ) as f:
        report = json.load(f)

    with CLAIM_PATH.open(
        "r",
        encoding="utf-8",
    ) as f:
        claim = json.load(f)

    expected = claim.get(
        "expected_result",
        {},
    )

    # ------------------------------------------------------------
    # 1. Canonical alpha
    # ------------------------------------------------------------

    spectral = report.get(
        "spectral_profile",
        {},
    )

    canonical_alpha = finite_float(
        spectral.get("estimated_alpha"),
        "spectral_profile.estimated_alpha",
    )

    # ------------------------------------------------------------
    # 2. Same-estimator identity guard
    #
    # These quantities are supposed to represent the same
    # canonical Welch estimator. A tolerance of 0.30 is NOT
    # scientifically acceptable here.
    # ------------------------------------------------------------

    cross_method = report.get(
        "cross_method_validation",
        {},
    )

    welch_alpha = finite_float(
        cross_method.get("welch_alpha"),
        "cross_method_validation.welch_alpha",
    )

    same_estimator_tol = float(
        expected.get(
            "max_same_estimator_disagreement",
            1e-8,
        )
    )

    welch_delta = abs(
        canonical_alpha -
        welch_alpha
    )

    require(
        welch_delta <= same_estimator_tol,
        (
            "canonical alpha and canonical Welch alpha are "
            "not numerically identical: "
            f"delta={welch_delta:.12f}, "
            f"allowed={same_estimator_tol:.12f}"
        ),
    )

    # ------------------------------------------------------------
    # 3. Statistical observed alpha must be the same canonical
    # measurement.
    # ------------------------------------------------------------

    statistical = report.get(
        "statistical_test",
        {},
    )

    statistical_alpha = finite_float(
        statistical.get("observed_alpha"),
        "statistical_test.observed_alpha",
    )

    statistical_delta = abs(
        canonical_alpha -
        statistical_alpha
    )

    require(
        statistical_delta <= same_estimator_tol,
        (
            "statistical_test.observed_alpha does not equal "
            "canonical alpha: "
            f"delta={statistical_delta:.12f}, "
            f"allowed={same_estimator_tol:.12f}"
        ),
    )

    # ------------------------------------------------------------
    # 4. Separation observed alpha must also be canonical.
    # ------------------------------------------------------------

    separation = (
        report.get("separation_test")
        or {}
    )

    separation_alpha = finite_float(
        separation.get("real_alpha"),
        "separation_test.real_alpha",
    )

    separation_delta = abs(
        canonical_alpha -
        separation_alpha
    )

    require(
        separation_delta <= same_estimator_tol,
        (
            "separation_test.real_alpha does not equal "
            "canonical alpha: "
            f"delta={separation_delta:.12f}, "
            f"allowed={same_estimator_tol:.12f}"
        ),
    )

    # ------------------------------------------------------------
    # 5. SCALE=1 MUST BE THE SAME CANONICAL MEASUREMENT.
    #
    # This is the critical guard.
    #
    # If scale=1 currently reports ~2.525 while canonical
    # reports ~0.953, this script MUST FAIL.
    #
    # We do not reinterpret that discrepancy.
    # We do not loosen the threshold.
    # We fix the scale-validation implementation.
    # ------------------------------------------------------------

    scale = report.get(
        "multi_scale_validation",
        {},
    )

    scale_primary = scale.get(
        "primary_scale_diagnostic",
        {},
    )

    scale_primary_alpha = finite_float(
        scale_primary.get("primary_alpha"),
        "multi_scale_validation.primary_scale_diagnostic.primary_alpha",
    )

    scale_delta = abs(
        canonical_alpha -
        scale_primary_alpha
    )

    require(
        scale_delta <= same_estimator_tol,
        (
            "SCALE=1 DOES NOT REPRODUCE THE CANONICAL ESTIMATOR: "
            f"canonical={canonical_alpha:.12f}, "
            f"scale1={scale_primary_alpha:.12f}, "
            f"delta={scale_delta:.12f}. "
            "Scale validation is scientifically invalid until "
            "the scale=1 implementation uses the exact canonical "
            "Welch estimator and frequency-band definition."
        ),
    )

    # ------------------------------------------------------------
    # 6. Scale dispersion is a separate criterion.
    # ------------------------------------------------------------

    scale_dispersion = scale.get(
        "dispersion",
        scale.get(
            "scale_dispersion",
            None,
        ),
    )

    if finite(scale_dispersion):

        max_scale_dispersion = float(
            expected.get(
                "max_scale_dispersion",
                0.40,
            )
        )

        require(
            float(scale_dispersion)
            <= max_scale_dispersion,
            (
                "scale dispersion exceeds declared threshold: "
                f"{float(scale_dispersion):.8f} > "
                f"{max_scale_dispersion:.8f}"
            ),
        )

    # ------------------------------------------------------------
    # 7. Bootstrap discrepancy remains diagnostic.
    #
    # It must be visible, but we do not silently convert it into
    # evidence for the claim.
    # ------------------------------------------------------------

    bootstrap = report.get(
        "bootstrap_center_discrepancy",
        {},
    )

    bootstrap_sigma = bootstrap.get(
        "std_units"
    )

    if finite(bootstrap_sigma):

        declared_bootstrap_limit = float(
            expected.get(
                "max_bootstrap_center_discrepancy_sigma",
                2.5,
            )
        )

        if float(bootstrap_sigma) > declared_bootstrap_limit:
            raise SystemExit(
                "❌ INTERNAL SCIENTIFIC CONSISTENCY FAILURE: "
                "bootstrap center discrepancy exceeds declared "
                "diagnostic threshold: "
                f"{float(bootstrap_sigma):.8f} > "
                f"{declared_bootstrap_limit:.8f}"
            )

    # ------------------------------------------------------------
    # 8. Consensus guard
    # ------------------------------------------------------------

    consensus = report.get(
        "consensus_guard",
        {},
    )

    if consensus.get("passed", False):

        agreement_delta = consensus.get(
            "agreement_delta"
        )

        require(
            finite(agreement_delta),
            "consensus agreement_delta is invalid",
        )

    # ------------------------------------------------------------
    # 9. Independent domains
    #
    # Consensus may count ONLY datasets explicitly marked
    # independent=True and valid=True.
    # ------------------------------------------------------------

    consensus_artifact = Path(
        "artifacts/canonical_consensus.json"
    )

    if consensus_artifact.exists():

        with consensus_artifact.open(
            "r",
            encoding="utf-8",
        ) as f:
            consensus_data = json.load(f)

        datasets = consensus_data.get(
            "datasets",
            [],
        )

        counted = [
            item
            for item in datasets
            if (
                item.get("independent") is True
                and item.get("valid") is True
                and item.get("role")
                in {
                    "primary_real",
                    "independent_real",
                }
            )
        ]

        declared_min_domains = int(
            expected.get(
                "min_independent_real_domains",
                2,
            )
        )

        require(
            len(counted) >= declared_min_domains,
            (
                "insufficient genuinely independent real "
                f"domains: {len(counted)} < "
                f"{declared_min_domains}"
            ),
        )

    # ------------------------------------------------------------
    # 10. Claim support cannot be activated merely because the
    # internal report looks good.
    #
    # External reproduction and adversarial validation remain
    # separate gates.
    # ------------------------------------------------------------

    scientific = report.get(
        "scientific_interpretation",
        {},
    )

    claim_support_gate = bool(
        scientific.get(
            "claim_support_gate",
            False,
        )
    )

    if claim_support_gate:

        reproducibility = scientific.get(
            "reproducibility",
            {},
        )

        require(
            reproducibility.get(
                "independent_rerun"
            ) == "verified",
            (
                "claim_support_gate=true while "
                "independent rerun is not verified"
            ),
        )

        require(
            bool(
                reproducibility.get(
                    "fingerprint_match",
                    False,
                )
            ),
            (
                "claim_support_gate=true while "
                "fingerprint_match=false"
            ),
        )

    # ------------------------------------------------------------
    # 11. Final output
    # ------------------------------------------------------------

    print(
        "✅ Canonical report internal consistency verified"
    )

    print(
        f"   canonical alpha: {canonical_alpha:.8f}"
    )

    print(
        f"   canonical Welch delta: "
        f"{welch_delta:.12f}"
    )

    print(
        f"   statistical alpha delta: "
        f"{statistical_delta:.12f}"
    )

    print(
        f"   separation alpha delta: "
        f"{separation_delta:.12f}"
    )

    print(
        f"   scale=1 alpha delta: "
        f"{scale_delta:.12f}"
    )

    if finite(bootstrap_sigma):

        print(
            "   bootstrap center discrepancy: "
            f"{float(bootstrap_sigma):.8f} sigma"
        )

    print(
        "✅ Scientific epistemic gate verified"
    )

if __name__ == "__main__":
    main()
