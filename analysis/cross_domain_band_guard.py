from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from analysis.load_real_datasets import DATASETS, load_series
from analysis.numerical_spectral_verification import estimate_alpha
from analysis.replication_computation_guard import (
    candidate_computation_gate,
    protocol_freeze_state,
)


CLAIM_PATH = Path("core-scientific/strict_claim.json")
PROVENANCE_PATH = Path("protocol/REPLICATION_PROVENANCE_REGISTRY_V1.json")
OUTPUT = Path("artifacts/cross_domain_band_guard.json")

PRIMARY_NAMES = {"sunspots"}
DERIVED_OR_CONTROL_NAMES = {"extended", "sunspots_global_extended"}


def load_inputs():
    if not CLAIM_PATH.is_file():
        raise SystemExit(f"Missing strict claim specification: {CLAIM_PATH}")
    if not PROVENANCE_PATH.is_file():
        raise SystemExit(f"Missing replication provenance registry: {PROVENANCE_PATH}")

    claim = json.loads(CLAIM_PATH.read_text(encoding="utf-8"))
    registry = json.loads(PROVENANCE_PATH.read_text(encoding="utf-8"))

    if registry.get("protocol") != "REPLICATION_PROVENANCE_REGISTRY_V1":
        raise SystemExit("Unexpected replication provenance registry protocol.")

    frozen, freeze_reasons = protocol_freeze_state(claim)
    policy = claim.get("dataset", {}).get("eligibility_policy", {})
    band = claim.get("scale_validation", {}).get("base_frequency_band", [0.01, 0.05])

    if not isinstance(band, list) or len(band) != 2:
        raise SystemExit("Invalid canonical frequency band.")

    freq_min, freq_max = float(band[0]), float(band[1])
    if not (0.0 < freq_min < freq_max < 0.5):
        raise SystemExit("Invalid canonical frequency band bounds.")

    return {
        "claim": claim,
        "candidates": registry.get("candidates", {}),
        "protocol_frozen": frozen,
        "protocol_freeze_reasons": freeze_reasons,
        "minimum_series_length": int(policy.get("minimum_series_length", 256)),
        "estimator_minimum_series_length": int(policy.get("estimator_minimum_series_length", 512)),
        "replication_minimum_series_length": int(policy.get("replication_minimum_series_length", 1024)),
        "minimum_frequency_bins": int(policy.get("minimum_frequency_bins", 20)),
        "canonical_nperseg": int(policy.get("canonical_nperseg", 1024)),
        "freq_min": freq_min,
        "freq_max": freq_max,
    }


def eligible_secondary_candidates(inputs):
    approved = []
    excluded = []

    for name, path in sorted(DATASETS.items()):
        if name in PRIMARY_NAMES or name in DERIVED_OR_CONTROL_NAMES:
            continue

        candidate = inputs["candidates"].get(name)
        allowed, reasons = candidate_computation_gate(
            candidate,
            path,
            inputs["protocol_frozen"],
        )

        if allowed:
            approved.append({"name": name, "path": path, "candidate": candidate})
        else:
            excluded.append({
                "name": name,
                "path": path,
                "status": "SKIPPED",
                "reasons": reasons,
            })

    return approved, excluded


def evaluate_approved_domain(item, inputs):
    series = load_series(item["path"])
    rows = int(len(series))

    if rows < inputs["minimum_series_length"]:
        return {
            "name": item["name"],
            "path": item["path"],
            "status": "INELIGIBLE_MEASUREMENT",
            "rows": rows,
            "alpha": None,
            "reason": "series_length_below_measurement_minimum",
        }

    if rows < inputs["estimator_minimum_series_length"]:
        return {
            "name": item["name"],
            "path": item["path"],
            "status": "INELIGIBLE_ESTIMATOR",
            "rows": rows,
            "alpha": None,
            "reason": "series_length_below_estimator_minimum",
        }

    if rows < inputs["replication_minimum_series_length"]:
        return {
            "name": item["name"],
            "path": item["path"],
            "status": "INELIGIBLE_REPLICATION",
            "rows": rows,
            "alpha": None,
            "reason": "series_length_below_replication_minimum",
        }

    nperseg = min(inputs["canonical_nperseg"], rows)
    frequencies = np.fft.rfftfreq(nperseg)
    available_bins = int(np.sum(
        (frequencies > inputs["freq_min"])
        & (frequencies < inputs["freq_max"])
    ))
    if available_bins < inputs["minimum_frequency_bins"]:
        return {
            "name": item["name"],
            "path": item["path"],
            "status": "INELIGIBLE_FREQUENCY_RESOLUTION",
            "rows": rows,
            "frequency_bins": available_bins,
            "alpha": None,
            "reason": "insufficient_frequency_bins",
        }

    alpha = float(estimate_alpha(
        series,
        freq_min=inputs["freq_min"],
        freq_max=inputs["freq_max"],
    ))
    if not np.isfinite(alpha):
        return {
            "name": item["name"],
            "path": item["path"],
            "status": "INVALID_ESTIMATOR",
            "rows": rows,
            "frequency_bins": available_bins,
            "alpha": None,
            "reason": "nonfinite_alpha",
        }

    return {
        "name": item["name"],
        "path": item["path"],
        "status": "COMPUTED_AFTER_GATES",
        "rows": rows,
        "frequency_bins": available_bins,
        "alpha": alpha,
    }


def main():
    inputs = load_inputs()
    approved, excluded = eligible_secondary_candidates(inputs)

    report = {
        "schema": "CROSS_DOMAIN_BAND_GUARD_V2",
        "status": "SKIPPED",
        "scientific_role": "diagnostic_only",
        "claim_authority": False,
        "promotion_authority": False,
        "scientific_inputs_modified": False,
        "confirmatory_protocol_frozen": inputs["protocol_frozen"],
        "protocol_freeze_reasons": inputs["protocol_freeze_reasons"],
        "minimum_approved_domains_required_before_computation": 2,
        "approved_candidate_count": len(approved),
        "computed_domains": [],
        "excluded_or_unapproved_domains": excluded,
        "reason": None,
    }

    # Fail closed: do not calculate or print alpha values unless at least
    # two domains independently pass the frozen-protocol and approval gates.
    if not inputs["protocol_frozen"]:
        report["reason"] = "confirmatory_protocol_not_frozen"
    elif len(approved) < 2:
        report["reason"] = "fewer_than_two_explicitly_approved_domains"

    if report["reason"] is None:
        computed = [
            evaluate_approved_domain(item, inputs)
            for item in approved
        ]
        report["computed_domains"] = computed
        valid = [
            item["alpha"]
            for item in computed
            if item.get("status") == "COMPUTED_AFTER_GATES"
            and item.get("alpha") is not None
        ]

        if len(valid) < 2:
            report["status"] = "SKIPPED"
            report["reason"] = "fewer_than_two_domains_passed_measurement_and_estimator_checks"
        else:
            median = float(np.median(valid))
            std = float(np.std(valid))
            report["summary"] = {
                "median_alpha": median,
                "alpha_std": std,
                "maximum_allowed_std": 1.8,
            }
            report["status"] = (
                "DIAGNOSTIC_PASS" if std <= 1.8 else "DIAGNOSTIC_FAIL"
            )
            report["reason"] = "diagnostic_only; does not establish replication or claim support"

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    if report["status"] == "SKIPPED":
        print("CROSS-DOMAIN BAND GUARD: SKIPPED")
        print("Reason:", report["reason"])
        print("No secondary alpha values were computed or emitted.")
        print("Report:", OUTPUT)
        return

    print("CROSS-DOMAIN BAND GUARD:", report["status"])
    for item in report["computed_domains"]:
        if item.get("status") == "COMPUTED_AFTER_GATES":
            print(f"{item['name']}: {item['alpha']:.6f}")
        else:
            print(f"{item['name']}: {item['status']} ({item.get('reason', 'no detail')})")
    print("Report:", OUTPUT)


if __name__ == "__main__":
    main()
