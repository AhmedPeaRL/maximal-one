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

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()

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

def finite(value) -> bool:
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False

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

    checks = {
        "alpha_within_declared_range":
            alpha_min <= alpha <= alpha_max,

        "sigma_within_declared_bound":
            sigma <= max_sigma,

        "p_value_within_declared_bound":
            p_value <= max_p_value,

        "cross_method_delta_within_bound":
            method_delta <= max_method_delta,

        "scale_dispersion_within_bound":
            finite(scale_dispersion)
            and scale_dispersion <= max_scale_dispersion,

        "minimum_independent_real_domains_met":
            independent_domains >= min_domains,

        "bootstrap_center_discrepancy_within_bound":
            bootstrap_discrepancy <= max_bootstrap_discrepancy,

        "scale_validation_passed":
            bool(scale.get("valid", False)),

        "scale_invariance_passed":
            bool(scale.get("scale_invariant", False)),

        "null_rejected":
            bool(report.get("null_rejected", False)),
    }

    passed = all(checks.values())

    return {
        "passed": bool(passed),

        "checks": checks,

        "measured": {
            "alpha": alpha,
            "sigma": sigma,
            "p_value": p_value,
            "cross_method_delta": method_delta,
            "scale_dispersion": scale_dispersion,
            "independent_real_domains": independent_domains,
            "bootstrap_center_discrepancy_sigma":
                bootstrap_discrepancy,
        },

        "declared_limits": {
            "alpha_range": [
                alpha_min,
                alpha_max,
            ],
            "max_sigma": max_sigma,
            "max_p_value": max_p_value,
            "max_method_delta": max_method_delta,
            "max_scale_dispersion":
                max_scale_dispersion,
            "min_independent_real_domains":
                min_domains,
            "max_bootstrap_center_discrepancy_sigma":
                max_bootstrap_discrepancy,
        },
    }

def load_collapse() -> dict:
    path = Path("artifacts/collapse_test.json")

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

    report = load_json(REPORT_PATH)
    strict_claim = load_json(STRICT_CLAIM_PATH)

    integrity = verify_report_integrity()

    contract = validate_strict_contract(
        report,
        strict_claim,
    )

    return {
        "timestamp": time.time(),

        "source": "independent_layer",

        "authority": {
            "authoritative_claim_contract":
                "core-scientific/strict_claim.json",

            "diagnostic_mirror":
                "core-scientific/unified_claim.json",

            "diagnostic_mirror_is_authoritative":
                False,
        },

        "verification_role":
            "contract_and_integrity_verification",

        "scientific_claim_decision": {
            "made_here": False,
            "status": "under_investigation",
            "reason":
                "This verifier validates declared contract "
                "conditions and report integrity. It does not "
                "independently promote the scientific claim "
                "to supported status.",
        },

        "integrity": integrity,

        "strict_contract": contract,

        "collapse_status": load_collapse(),

        "adaptive_thresholds": {
            "used": False,
            "reason":
                "Scientific acceptance boundaries are read "
                "only from strict_claim.json. Observed data "
                "are never used to construct acceptance "
                "thresholds.",
        },

        "epistemic_guard": {
            "confidence_as_probability": False,
            "adaptive_truth_threshold": False,
            "automatic_claim_acceptance": False,
            "mechanism_inferred": False,
            "hcm_causation_inferred": False,
            "universality_inferred": False,
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

    print("Independent verification written.")
    print(
        "Authoritative contract: "
        "core-scientific/strict_claim.json"
    )
    print("Adaptive thresholds used: False")
    print(
        "Scientific claim promotion by this verifier: False"
    )
    print(
        "Contract checks passed:",
        record["strict_contract"]["passed"],
    )
    print(
        "Report integrity passed:",
        record["integrity"]["passed"],
    )

    if not record["integrity"]["passed"]:
        raise SystemExit(
            "❌ Report integrity verification failed."
        )
