from __future__ import annotations

import hashlib
import json
import math
import os
import time
from pathlib import Path

REPORT_PATH = Path("artifacts/canonical_report.json")
STRICT_CLAIM_PATH = Path("core-scientific/strict_claim.json")
OUTPUT_PATH = Path("public/independent_verification.json")

def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()

def finite(value) -> bool:
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False

def load_stored_report_hash() -> tuple[str, str]:
    candidates = (
        Path("artifacts/report.hash"),
        Path("report.hash"),
    )

    for path in candidates:
        if path.exists():
            value = path.read_text(encoding="utf-8").strip()

            if value:
                return value, str(path)

    raise FileNotFoundError(
        "No report.hash found in artifacts/report.hash or report.hash"
    )

def verify_report_integrity() -> dict:
    if not REPORT_PATH.exists():
        raise FileNotFoundError(
            "artifacts/canonical_report.json is missing"
        )

    stored_hash, hash_source = load_stored_report_hash()
    calculated_hash = sha256_file(REPORT_PATH)

    return {
        "passed": stored_hash == calculated_hash,
        "stored_hash": stored_hash,
        "calculated_hash": calculated_hash,
        "hash_source": hash_source,
    }

def read_external_replay_status(report: dict) -> dict:
    """
    Read the canonical independent clean-checkout
    reproducibility attestation.

    This artifact proves only:
      - fresh public repository checkout
      - exact workflow commit
      - canonical input reconstruction
      - independent canonical rerun
      - normalized full-report comparison
      - fingerprint equality

    It does NOT prove:
      - external laboratory replication
      - independent execution environment
      - mechanism
      - universality
      - HCM causation
      - scientific claim promotion
    """

    path = Path(
        "artifacts/external_replay_verification.json"
    )

    if not path.exists():
        return {
            "available": False,
            "independent_rerun_verified": False,
            "fingerprint_verified": False,
            "structure_match": False,
            "verification_method": None,
            "scientific_role": None,
            "status": "not_available",
            "available_and_verified": False,
            "source": str(path),
        }

    try:
        data = load_json(path)

        independent_rerun_verified = (
            data.get(
                "independent_replay_verified",
                False,
            )
            is True
        )

        fingerprint_verified = (
            data.get(
                "fingerprint_match",
                False,
            )
            is True
        )

        structure_match = (
            data.get(
                "structure_match",
                False,
            )
            is True
        )

        verification_method = data.get(
            "comparison_method"
        )

        scientific_role = data.get(
            "scientific_role"
        )

        valid_method = (
            verification_method
            ==
            "normalized_full_canonical_report"
        )

        valid_role = (
            scientific_role
            ==
            "independent_clean_checkout_reproducibility_gate"
        )

        verified = bool(
            independent_rerun_verified
            and fingerprint_verified
            and structure_match
            and valid_method
            and valid_role
            and data.get("status") == "verified"
        )

        return {
            "available": True,

            "independent_rerun_verified": bool(
                independent_rerun_verified
                and structure_match
                and valid_method
                and valid_role
                and data.get("status") == "verified"
            ),

            "fingerprint_verified": bool(
                fingerprint_verified
                and structure_match
                and valid_method
                and valid_role
                and data.get("status") == "verified"
            ),

            "structure_match": structure_match,

            "verification_method":
                verification_method,

            "scientific_role":
                scientific_role,

            "status":
                data.get("status", "unknown"),

            "available_and_verified":
                verified,

            "source":
                str(path),
        }

    except Exception as exc:
        return {
            "available": True,
            "independent_rerun_verified": False,
            "fingerprint_verified": False,
            "structure_match": False,
            "verification_method": None,
            "scientific_role": None,
            "status": "unreadable",
            "available_and_verified": False,
            "source": str(path),
            "error": str(exc),
        }        

def read_adversarial_status() -> dict:
    path = Path("artifacts/adversarial_control.json")

    if not path.exists():
        return {
            "available": False,
            "passed": False,
            "status": "not_available",
        }

    try:
        data = load_json(path)

        passed = (
            data.get("passed", False) is True
        )

        return {
            "available": True,
            "passed": passed,
            "status": (
                "passed"
                if passed
                else "failed"
            ),
        }

    except Exception as exc:
        return {
            "available": True,
            "passed": False,
            "status": "unreadable",
            "error": str(exc),
        }

def validate_strict_contract(
    report: dict,
    strict_claim: dict,
) -> dict:

    expected = strict_claim["expected_result"]

    alpha = float(
        report["spectral_profile"]["estimated_alpha"]
    )

    sigma = float(
        report["spectral_profile"]["bootstrap_std"]
    )

    p_value = float(
        report["statistical_test"]["p_value"]
    )

    method_delta = float(
        report["cross_method_validation"]["agreement_delta"]
    )

    scale = report["multi_scale_validation"]

    scale_dispersion = float(
        scale.get(
            "dispersion",
            scale.get("relative_spread")
        )
    )

    independent_domains = int(
        report["consensus_guard"]["independent_real_domains"]
    )

    bootstrap_discrepancy = float(
        report["bootstrap_center_discrepancy"]["std_units"]
    )

    alpha_min, alpha_max = map(
        float,
        expected["alpha_range"]
    )

    max_sigma = float(
        expected["max_sigma"]
    )

    max_method_delta = float(
        expected["max_method_delta"]
    )

    max_scale_dispersion = float(
        expected["max_scale_dispersion"]
    )

    max_p_value = float(
        expected["max_p_value"]
    )

    min_domains = int(
        expected["min_independent_real_domains"]
    )

    max_bootstrap_discrepancy = float(
        expected.get(
            "max_bootstrap_center_discrepancy_sigma",
            2.5,
        )
    )

    max_cross_domain_std = float(
        expected.get(
            "max_cross_domain_std",
            1.2,
        )
    )

    cross_domain = report.get(
        "cross_domain_replication",
        {},
    )

    cross_domain_std = cross_domain.get(
        "real_domain_std"
    )

    cross_domain_std_passed = (
        finite(cross_domain_std)
        and
        float(cross_domain_std)
        <= max_cross_domain_std
    )

    independent_domains_passed = (
        independent_domains
        >= min_domains
    )

    external_replay = read_external_replay_status(
        report
    )

    adversarial = read_adversarial_status()

    # ------------------------------------------------------------
    # CORE CONTRACT CHECKS
    #
    # These are the checks that evaluate whether the generated
    # report satisfies the declared empirical contract.
    #
    # External replay and adversarial control are reported
    # separately because they are evidence-completion layers,
    # not properties of the numerical report itself.
    # ------------------------------------------------------------

    contract_checks = {
        "alpha_within_declared_range":
            finite(alpha)
            and
            alpha_min <= alpha <= alpha_max,

        "sigma_within_declared_bound":
            finite(sigma)
            and
            sigma <= max_sigma,

        "p_value_within_declared_bound":
            finite(p_value)
            and
            p_value <= max_p_value,

        "cross_method_delta_within_bound":
            finite(method_delta)
            and
            method_delta <= max_method_delta,

        "scale_dispersion_within_bound":
            finite(scale_dispersion)
            and
            scale_dispersion <= max_scale_dispersion,

        "minimum_independent_real_domains_met":
            independent_domains_passed,

        "cross_domain_std_within_bound":
            cross_domain_std_passed,

        "bootstrap_center_discrepancy_within_bound":
            finite(bootstrap_discrepancy)
            and
            bootstrap_discrepancy
            <= max_bootstrap_discrepancy,

        "scale_validation_passed":
            bool(scale.get("valid", False)),

        "scale_invariance_passed":
            bool(scale.get("scale_invariant", False)),

        "null_rejected":
            bool(report.get("null_rejected", False)),
    }

    contract_passed = all(
        contract_checks.values()
    )

    # ------------------------------------------------------------
    # EVIDENCE-COMPLETION CHECKS
    #
    # These remain explicit blockers for final scientific support.
    # They are NOT silently converted into numerical success.
    # ------------------------------------------------------------

    evidence_completion_checks = {
        "independent_rerun_verified":
            external_replay[
                "independent_rerun_verified"
            ],

        "fingerprint_verified":
            external_replay[
                "fingerprint_verified"
            ],

        "adversarial_control_passed":
            adversarial[
                "passed"
            ],
    }

    evidence_completion = all(
        evidence_completion_checks.values()
    )

    # ------------------------------------------------------------
    # FINAL SUPPORT READINESS
    #
    # This is intentionally NOT a claim-promotion mechanism.
    # It only states whether every declared support layer is
    # present.
    # ------------------------------------------------------------

    support_ready = bool(
        contract_passed
        and
        evidence_completion
    )

    return {
        # --------------------------------------------------------
        # Compatibility field:
        #
        # The CI workflow currently reads:
        # strict_contract["passed"]
        #
        # This MUST mean only that the declared empirical
        # numerical/methodological contract passed.
        #
        # It does NOT mean that the scientific claim is supported.
        # Evidence-completion requirements remain separate below.
        # --------------------------------------------------------
        "passed": bool(contract_passed),

        "contract_passed": bool(
            contract_passed
        ),

        "evidence_completion_passed": bool(
            evidence_completion
        ),

        "support_ready": support_ready,

        "scope":
            "empirical_contract_only",

        "does_not_mean_scientific_claim_supported":
            True,

        "checks": {
            **contract_checks,
            **evidence_completion_checks,
        },

        "contract_checks": contract_checks,

        "evidence_completion_checks":
            evidence_completion_checks,

        "measured": {
            "alpha": alpha,
            "sigma": sigma,
            "p_value": p_value,
            "cross_method_delta":
                method_delta,
            "scale_dispersion":
                scale_dispersion,
            "independent_real_domains":
                independent_domains,
            "cross_domain_std":
                (
                    float(cross_domain_std)
                    if finite(cross_domain_std)
                    else None
                ),
            "bootstrap_center_discrepancy_sigma":
                bootstrap_discrepancy,
        },

        "declared_limits": {
            "alpha_range": [
                alpha_min,
                alpha_max,
            ],
            "max_sigma":
                max_sigma,
            "max_p_value":
                max_p_value,
            "max_method_delta":
                max_method_delta,
            "max_scale_dispersion":
                max_scale_dispersion,
            "max_cross_domain_std":
                max_cross_domain_std,
            "min_independent_real_domains":
                min_domains,
            "max_bootstrap_center_discrepancy_sigma":
                max_bootstrap_discrepancy,
        },

        "external_replay": external_replay,

        "adversarial_control": adversarial,
    }

def load_collapse() -> dict:
    path = Path(
        "artifacts/collapse_test.json"
    )

    if not path.exists():
        return {
            "available": False,
            "status": "not_available",
        }

    try:
        data = load_json(path)

        return {
            "available": True,
            "status": data.get(
                "collapse_test",
                "unknown",
            ),
        }

    except Exception as exc:
        return {
            "available": True,
            "status": "unreadable",
            "error": str(exc),
        }

def build_external_record():
    if not REPORT_PATH.exists():
        raise FileNotFoundError(
            "canonical_report.json is missing"
        )

    if not STRICT_CLAIM_PATH.exists():
        raise FileNotFoundError(
            "strict_claim.json is missing"
        )

    report = load_json(
        REPORT_PATH
    )

    strict_claim = load_json(
        STRICT_CLAIM_PATH
    )

    integrity = verify_report_integrity()

    contract = validate_strict_contract(
        report,
        strict_claim,
    )

    return {
        "timestamp": time.time(),

        "source":
            "independent_layer",

        "authority": {
            "authoritative_claim_contract":
                "core-scientific/strict_claim.json",

            "diagnostic_mirror":
                "core-scientific/unified_claim.json",

            "diagnostic_mirror_is_authoritative":
                False,
        },

        "verification_role":
            "contract_and_evidence_completion_verification",

        "scientific_claim_decision": {
            "made_here": False,

            "status":
                "under_investigation",

            "support_ready":
                bool(
                    contract["support_ready"]
                ),

            "reason":
                "This verifier evaluates the declared "
                "empirical contract and records evidence "
                "completion status. It does not independently "
                "promote the scientific claim.",
        },

        "integrity":
            integrity,

        "strict_contract":
            contract,

        "collapse_status":
            load_collapse(),

        "adaptive_thresholds": {
            "used": False,

            "reason":
                "Scientific acceptance boundaries are read "
                "only from strict_claim.json. Observed data "
                "are never used to construct acceptance "
                "thresholds.",
        },

        "epistemic_guard": {
            "confidence_as_probability":
                False,

            "adaptive_truth_threshold":
                False,

            "automatic_claim_acceptance":
                False,

            "mechanism_inferred":
                False,

            "hcm_causation_inferred":
                False,

            "universality_inferred":
                False,
        },
    }

if __name__ == "__main__":
    os.makedirs(
        "public",
        exist_ok=True,
    )

    record = build_external_record()

    with OUTPUT_PATH.open(
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            record,
            f,
            indent=2,
            sort_keys=True,
        )

    contract = record[
        "strict_contract"
    ]

    print(
        "Independent verification written."
    )

    print(
        "Authoritative contract: "
        "core-scientific/strict_claim.json"
    )

    print(
        "Adaptive thresholds used: False"
    )

    print(
        "Scientific claim promotion: NOT PERFORMED"
    )

    print(
        "Empirical contract passed:",
        contract["contract_passed"],
    )

    print(
        "Evidence completion passed:",
        contract[
            "evidence_completion_passed"
        ],
    )

    print(
        "Final support readiness:",
        contract["support_ready"],
    )

    print(
        "Report integrity passed:",
        record["integrity"]["passed"],
    )

    if not record["integrity"]["passed"]:
        raise SystemExit(
            "❌ Report integrity verification failed."
        )
