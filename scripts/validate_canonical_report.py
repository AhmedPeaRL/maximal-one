from __future__ import annotations
import json
import math
import sys
from pathlib import Path

REPORT_PATH = Path("artifacts/canonical_report.json")
CLAIM_PATH = Path("core-scientific/strict_claim.json")

def finite(value):
    return isinstance(value, (int, float)) and math.isfinite(float(value))

def require(condition, message):
    if not condition:
        raise SystemExit(f"❌ INTERNAL SCIENTIFIC CONSISTENCY FAILURE: {message}")

def main():
    require(REPORT_PATH.exists(), f"missing report: {REPORT_PATH}")
    require(CLAIM_PATH.exists(), f"missing claim specification: {CLAIM_PATH}")

    with REPORT_PATH.open("r", encoding="utf-8") as f:
        report = json.load(f)

    with CLAIM_PATH.open("r", encoding="utf-8") as f:
        claim = json.load(f)

    max_delta = float(
        claim["expected_result"].get(
            "max_internal_alpha_disagreement",
            0.30,
        )
    )

    spectral = report.get("spectral_profile", {})
    cross_method = report.get("cross_method_validation", {})
    separation = report.get("separation_test") or {}
    statistical = report.get("statistical_test", {})
    scale = report.get("multi_scale_validation", {})
    consensus = report.get("consensus_guard", {})

    canonical_alpha = spectral.get("estimated_alpha")

    require(
        finite(canonical_alpha),
        f"canonical spectral alpha is invalid: {canonical_alpha}",
    )

    canonical_alpha = float(canonical_alpha)

    observations = {
        "spectral_profile.estimated_alpha": canonical_alpha,
        "statistical_test.observed_alpha": statistical.get(
            "observed_alpha"
        ),
        "separation_test.real_alpha": separation.get(
            "real_alpha"
        ),
        "cross_method_validation.welch_alpha": cross_method.get(
            "welch_alpha"
        ),
    }

    for name, value in observations.items():
        require(
            finite(value),
            f"{name} is missing or non-finite: {value}",
        )

    disagreements = {}

    for name, value in observations.items():
        delta = abs(canonical_alpha - float(value))
        disagreements[name] = delta

        require(
            delta <= max_delta,
            (
                f"{name} disagrees with canonical alpha by "
                f"{delta:.8f}; maximum allowed is {max_delta:.8f}"
            ),
        )

    bootstrap = report.get("bootstrap_center_discrepancy", {})
    bootstrap_sigma = bootstrap.get("std_units")

    if finite(bootstrap_sigma):
        max_bootstrap_sigma = float(
            claim["expected_result"].get(
                "max_bootstrap_center_discrepancy_sigma",
                2.5,
            )
        )

        require(
            float(bootstrap_sigma) <= max_bootstrap_sigma,
            (
                "bootstrap center discrepancy exceeds declared "
                f"scientific tolerance: {bootstrap_sigma:.8f} > "
                f"{max_bootstrap_sigma:.8f}"
            ),
        )

    scale_primary = scale.get("primary_scale_diagnostic", {})
    scale_primary_alpha = scale_primary.get("primary_alpha")

    if finite(scale_primary_alpha):
        scale_delta = abs(
            canonical_alpha - float(scale_primary_alpha)
        )

        require(
            scale_delta <= max_delta,
            (
                "scale validation primary alpha is inconsistent "
                f"with canonical alpha: delta={scale_delta:.8f}"
            ),
        )

    # Consensus must never silently convert an inconsistent report
    # into a supported scientific claim.
    if consensus.get("passed", False):
        require(
            finite(consensus.get("agreement_delta")),
            "consensus agreement_delta is invalid",
        )

    # Final epistemic guard.
    scientific = report.setdefault(
        "scientific_interpretation",
        {},
    )

    claim_support_gate = bool(
        scientific.get("claim_support_gate", False)
    )

    if claim_support_gate:
        required_external = (
            scientific.get("reproducibility", {})
            .get("independent_rerun")
        )

        require(
            required_external == "verified",
            (
                "claim_support_gate=true while independent rerun "
                "is not verified"
            ),
        )

        require(
            bool(
                scientific.get("reproducibility", {})
                .get("fingerprint_match", False)
            ),
            (
                "claim_support_gate=true while fingerprint_match "
                "is false"
            ),
        )

    print("✅ Canonical report internal consistency verified")
    print(f"   canonical alpha: {canonical_alpha:.8f}")

    for name, delta in disagreements.items():
        print(
            f"   {name}: delta={delta:.8f}"
        )

    if finite(bootstrap_sigma):
        print(
            f"   bootstrap center discrepancy: "
            f"{float(bootstrap_sigma):.8f} sigma"
        )

    if finite(scale_primary_alpha):
        print(
            f"   scale primary alpha: "
            f"{float(scale_primary_alpha):.8f}"
        )

    print("✅ Scientific epistemic gate verified")

if __name__ == "__main__":
    main()
