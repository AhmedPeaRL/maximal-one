from __future__ import annotations
import json
import math
from pathlib import Path

REPORT_PATH = Path(
    "artifacts/canonical_report.json"
)

CLAIM_PATH = Path(
    "core-scientific/strict_claim.json"
)

CONSENSUS_PATH = Path(
    "artifacts/canonical_consensus.json"
)

def finite(value):
    return (
        isinstance(
            value,
            (int, float),
        )
        and math.isfinite(
            float(value)
        )
    )

def require(
    condition,
    message,
):
    if not condition:
        raise SystemExit(
            "❌ INTERNAL SCIENTIFIC CONSISTENCY "
            f"FAILURE: {message}"
        )

def finite_float(
    value,
    name,
):
    require(
        finite(value),
        f"{name} is missing or non-finite: {value}",
    )

    return float(value)

def exact_delta(
    a,
    b,
):
    return abs(
        float(a) -
        float(b)
    )

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

    same_estimator_tol = float(
        expected.get(
            "max_same_estimator_disagreement",
            1e-8,
        )
    )

    # ============================================================
    # 1. Canonical alpha
    # ============================================================

    spectral = report.get(
        "spectral_profile",
        {},
    )

    canonical_alpha = finite_float(
        spectral.get(
            "estimated_alpha"
        ),
        "spectral_profile.estimated_alpha",
    )

    # ============================================================
    # 2. Canonical Welch identity
    # ============================================================

    cross_method = report.get(
        "cross_method_validation",
        {},
    )

    welch_alpha = finite_float(
        cross_method.get(
            "welch_alpha"
        ),
        "cross_method_validation.welch_alpha",
    )

    welch_delta = exact_delta(
        canonical_alpha,
        welch_alpha,
    )

    require(
        welch_delta <= same_estimator_tol,
        (
            "canonical alpha and canonical Welch alpha "
            "do not represent the same numerical "
            "measurement: "
            f"delta={welch_delta:.12f}, "
            f"allowed={same_estimator_tol:.12f}"
        ),
    )

    # ============================================================
    # 3. Statistical alpha identity
    # ============================================================

    statistical = report.get(
        "statistical_test",
        {},
    )

    statistical_alpha = finite_float(
        statistical.get(
            "observed_alpha"
        ),
        "statistical_test.observed_alpha",
    )

    statistical_delta = exact_delta(
        canonical_alpha,
        statistical_alpha,
    )

    require(
        statistical_delta <= same_estimator_tol,
        (
            "statistical observed alpha does not "
            "equal canonical alpha: "
            f"delta={statistical_delta:.12f}"
        ),
    )

    # ============================================================
    # 4. Separation alpha identity
    # ============================================================

    separation = (
        report.get(
            "separation_test"
        )
        or {}
    )

    separation_alpha = finite_float(
        separation.get(
            "real_alpha"
        ),
        "separation_test.real_alpha",
    )

    separation_delta = exact_delta(
        canonical_alpha,
        separation_alpha,
    )

    require(
        separation_delta <= same_estimator_tol,
        (
            "separation real alpha does not "
            "equal canonical alpha: "
            f"delta={separation_delta:.12f}"
        ),
    )

    # ============================================================
    # 5. SCALE=1 IDENTITY
    #
    # This is a hard scientific gate.
    #
    # Scale=1 is not allowed to be merely "similar".
    # It must reproduce the exact canonical estimator.
    # ============================================================

    scale = report.get(
        "multi_scale_validation",
        {},
    )

    scale_primary = scale.get(
        "primary_scale_diagnostic",
        {},
    )

    scale_primary_alpha = finite_float(
        scale_primary.get(
            "primary_alpha"
        ),
        (
            "multi_scale_validation."
            "primary_scale_diagnostic."
            "primary_alpha"
        ),
    )

    scale_delta = exact_delta(
        canonical_alpha,
        scale_primary_alpha,
    )

    require(
        scale_delta <= same_estimator_tol,
        (
            "SCALE=1 DOES NOT REPRODUCE THE "
            "CANONICAL ESTIMATOR: "
            f"canonical={canonical_alpha:.12f}, "
            f"scale1={scale_primary_alpha:.12f}, "
            f"delta={scale_delta:.12f}. "
            "The scale-validation implementation "
            "must be repaired before this report can "
            "be considered internally valid."
        ),
    )

    # ============================================================
    # 6. If explicit scale entries exist, verify scale=1.
    # ============================================================

    scale_entries = scale.get(
        "scales",
        [],
    )

    if isinstance(
        scale_entries,
        list,
    ):

        scale_one = None

        for item in scale_entries:

            if not isinstance(
                item,
                dict,
            ):
                continue

            value = item.get(
                "scale",
                item.get(
                    "factor"
                ),
            )

            if finite(value):

                if float(value) == 1.0:
                    scale_one = item
                    break

        if scale_one is not None:

            scale_one_alpha = (
                scale_one.get(
                    "alpha",
                    scale_one.get(
                        "estimated_alpha"
                    ),
                )
            )

            scale_one_alpha = finite_float(
                scale_one_alpha,
                "multi_scale_validation.scale=1.alpha",
            )

            scale_one_delta = exact_delta(
                canonical_alpha,
                scale_one_alpha,
            )

            require(
                scale_one_delta
                <= same_estimator_tol,
                (
                    "explicit scale=1 alpha does "
                    "not reproduce canonical alpha: "
                    f"delta={scale_one_delta:.12f}"
                ),
            )

    # ============================================================
    # 7. Scale dispersion
    #
    # This remains a secondary diagnostic.
    # ============================================================

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
                "scale dispersion exceeds "
                "declared threshold: "
                f"{float(scale_dispersion):.8f} > "
                f"{max_scale_dispersion:.8f}"
            ),
        )

    # ============================================================
    # 8. Bootstrap diagnostic
    # ============================================================

    bootstrap = report.get(
        "bootstrap_center_discrepancy",
        {},
    )

    bootstrap_sigma = bootstrap.get(
        "std_units"
    )

    if finite(bootstrap_sigma):

        limit = float(
            expected.get(
                "max_bootstrap_center_discrepancy_sigma",
                2.5,
            )
        )

        require(
            float(bootstrap_sigma) <= limit,
            (
                "bootstrap center discrepancy "
                "exceeds declared diagnostic limit: "
                f"{float(bootstrap_sigma):.8f} > "
                f"{limit:.8f}"
            ),
        )

    # ============================================================
    # 9. Consensus artifact
    # ============================================================

    if CONSENSUS_PATH.exists():

        with CONSENSUS_PATH.open(
            "r",
            encoding="utf-8",
        ) as f:
            consensus = json.load(f)

        datasets = consensus.get(
            "datasets",
            [],
        )

        counted = [
            item
            for item in datasets
            if (
                item.get(
                    "independent"
                ) is True
                and item.get(
                    "valid"
                ) is True
                and item.get(
                    "role"
                )
                in {
                    "primary_real",
                    "independent_real",
                }
            )
        ]

        excluded = consensus.get(
            "excluded_real_domains"
        )

        require(
            isinstance(
                excluded,
                list,
            ),
            (
                "consensus artifact must explicitly "
                "report excluded_real_domains"
            ),
        )

        declared_min = int(
            expected.get(
                "min_independent_real_domains",
                2,
            )
        )

        require(
            len(counted) >= declared_min,
            (
                "insufficient genuinely independent "
                f"real domains: {len(counted)} < "
                f"{declared_min}"
            ),
        )

    # ============================================================
    # 10. Claim-support gate
    #
    # Internal consistency is NOT external replication.
    # ============================================================

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

    # ============================================================
    # 11. Final
    # ============================================================

    print(
        "✅ Canonical report internal "
        "consistency verified"
    )

    print(
        f"   canonical alpha: "
        f"{canonical_alpha:.8f}"
    )

    print(
        f"   Welch identity delta: "
        f"{welch_delta:.12f}"
    )

    print(
        f"   statistical identity delta: "
        f"{statistical_delta:.12f}"
    )

    print(
        f"   separation identity delta: "
        f"{separation_delta:.12f}"
    )

    print(
        f"   scale=1 identity delta: "
        f"{scale_delta:.12f}"
    )

    if finite(bootstrap_sigma):

        print(
            "   bootstrap discrepancy: "
            f"{float(bootstrap_sigma):.8f} sigma"
        )

    print(
        "✅ Scientific epistemic gate verified"
    )

if __name__ == "__main__":
    main()
