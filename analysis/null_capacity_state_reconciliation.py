#!/usr/bin/env python3
"""Reconcile null-capacity diagnostics by source and protocol identity.

The static strict-claim value is compared with the dedicated primary-null
capacity audit. The canonical report and null-calibration gate are compared
with each other because the latter copies the former's estimate. Estimates
from different Monte Carlo seeds are recorded as separate estimates, not
required to be numerically identical. This tool is diagnostic-only and never
changes scientific inputs, thresholds, eligibility, or promotion authority.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

STRICT_CLAIM = Path("core-scientific/strict_claim.json")
CANONICAL_REPORT = Path("artifacts/canonical_report.json")
NULL_GATE = Path("artifacts/null_calibration_gate.json")
PRIMARY_AUDIT = Path("artifacts/primary_null_capacity_audit.json")
OUTPUT = Path("artifacts/null_capacity_state_reconciliation.json")


def nested(data: dict[str, Any], *keys: str) -> Any:
    value: Any = data
    for key in keys:
        if not isinstance(value, dict) or key not in value:
            return None
        value = value[key]
    return value


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def close_enough(left: Any, right: Any, tolerance: float = 1e-12) -> bool | None:
    if not is_number(left) or not is_number(right):
        return None
    return abs(float(left) - float(right)) <= tolerance


def build_report(
    strict_claim: dict[str, Any],
    canonical: dict[str, Any],
    null_gate: dict[str, Any],
    primary_audit: dict[str, Any] | None = None,
) -> dict[str, Any]:
    static_review = nested(strict_claim, "stochastic_null_protocol", "model_capacity_review") or {}
    canonical_null = nested(canonical, "appropriate_stochastic_null") or {}
    canonical_diag = canonical_null.get("order_selection_diagnostic") or {}
    gate_diag = null_gate.get("canonical_null_diagnostics") or {}
    audit = primary_audit or {}

    static_fraction = static_review.get("surrogate_boundary_fraction")
    canonical_fraction = canonical_diag.get("surrogate_boundary_fraction")
    gate_fraction = gate_diag.get("surrogate_boundary_fraction")
    audit_fraction = audit.get("surrogate_boundary_fraction")

    static_order = static_review.get("observed_selected_order")
    canonical_order = canonical_null.get("selected_order")
    gate_order = gate_diag.get("selected_order")
    audit_order = audit.get("observed_selected_order")

    static_max = static_review.get("maximum_declared_order")
    gate_max = nested(null_gate, "protocol", "max_order")
    audit_max = audit.get("max_order")

    audit_present = primary_audit is not None
    static_audit_fraction_match = close_enough(static_fraction, audit_fraction) if audit_present else None
    static_audit_order_match = (static_order == audit_order) if audit_present and isinstance(static_order, int) and isinstance(audit_order, int) else None
    static_audit_max_match = (static_max == audit_max) if audit_present and isinstance(static_max, int) and isinstance(audit_max, int) else None
    canonical_gate_fraction_match = close_enough(canonical_fraction, gate_fraction)
    canonical_gate_order_match = (canonical_order == gate_order) if isinstance(canonical_order, int) and isinstance(gate_order, int) else None
    static_gate_max_match = (static_max == gate_max) if isinstance(static_max, int) and isinstance(gate_max, int) else None

    audit_protocol = audit.get("protocol_revision")
    gate_protocol = nested(null_gate, "protocol", "protocol_revision")
    audit_seed = audit.get("seed")
    canonical_seed = nested(canonical, "metadata", "seed")
    # Seed metadata may not exist in every canonical report. Never infer it.
    different_seed_known = is_number(audit_seed) and is_number(canonical_seed) and audit_seed != canonical_seed

    checks = [static_audit_fraction_match, static_audit_order_match, static_audit_max_match,
              canonical_gate_fraction_match, canonical_gate_order_match, static_gate_max_match]
    checks_complete = all(value is not None for value in checks)
    source_scoped_match = checks_complete and all(value is True for value in checks)

    if not audit_present:
        status = "RECONCILIATION_REQUIRED_PRIMARY_AUDIT_MISSING"
    elif source_scoped_match:
        status = "SOURCE_SCOPED_ESTIMATES_RECONCILED"
    else:
        status = "RECONCILIATION_REQUIRED"

    return {
        "protocol": "NULL_CAPACITY_STATE_RECONCILIATION_V2",
        "status": status,
        "diagnostic_only": True,
        "claim_support": False,
        "promotion_authority": False,
        "scientific_inputs_modified": False,
        "values": {
            "strict_claim_surrogate_boundary_fraction": static_fraction,
            "primary_audit_surrogate_boundary_fraction": audit_fraction,
            "canonical_report_surrogate_boundary_fraction": canonical_fraction,
            "null_gate_surrogate_boundary_fraction": gate_fraction,
            "strict_claim_observed_order": static_order,
            "primary_audit_observed_order": audit_order,
            "canonical_report_selected_order": canonical_order,
            "null_gate_selected_order": gate_order,
            "strict_claim_maximum_order": static_max,
            "primary_audit_maximum_order": audit_max,
            "null_gate_maximum_order": gate_max,
            "primary_audit_seed": audit_seed,
            "canonical_report_seed_if_explicitly_recorded": canonical_seed,
            "primary_audit_protocol_revision": audit_protocol,
            "null_gate_protocol_revision": gate_protocol,
        },
        "comparisons": {
            "strict_claim_matches_primary_audit_fraction_within_1e-12": static_audit_fraction_match,
            "strict_claim_matches_primary_audit_observed_order": static_audit_order_match,
            "strict_claim_matches_primary_audit_maximum_order": static_audit_max_match,
            "canonical_report_matches_null_gate_fraction_within_1e-12": canonical_gate_fraction_match,
            "canonical_report_matches_null_gate_selected_order": canonical_gate_order_match,
            "strict_claim_matches_null_gate_maximum_order": static_gate_max_match,
        },
        "interpretation": (
            "The static specification matches the dedicated primary audit, and the null gate matches the canonical report. "
            "The boundary fractions from the dedicated audit and canonical report are source-scoped Monte Carlo estimates; "
            "they are not required to be identical when generated from different random streams/seeds. Their values are retained separately."
            if source_scoped_match else
            "A required source is missing or one or more within-source comparisons differ. Preserve every source value and reconcile exact commit, artifact, seed, protocol, and run identity. Do not edit the static specification or scientific thresholds from this diagnostic."
        ),
        "different_seed_explicitly_recorded": different_seed_known,
        "cross_source_fraction_difference": (
            float(audit_fraction) - float(canonical_fraction)
            if is_number(audit_fraction) and is_number(canonical_fraction) else None
        ),
    }


def main() -> int:
    paths = {"strict_claim": STRICT_CLAIM, "canonical_report": CANONICAL_REPORT, "null_gate": NULL_GATE}
    missing = [str(path) for path in paths.values() if not path.is_file()]
    if missing:
        report = {
            "protocol": "NULL_CAPACITY_STATE_RECONCILIATION_V2",
            "status": "INPUTS_MISSING",
            "diagnostic_only": True,
            "claim_support": False,
            "promotion_authority": False,
            "scientific_inputs_modified": False,
            "missing_inputs": missing,
            "interpretation": "Required source JSON is missing; no comparison was made.",
        }
    else:
        loaded = {name: json.loads(path.read_text(encoding="utf-8")) for name, path in paths.items()}
        primary_audit = json.loads(PRIMARY_AUDIT.read_text(encoding="utf-8")) if PRIMARY_AUDIT.is_file() else None
        report = build_report(loaded["strict_claim"], loaded["canonical_report"], loaded["null_gate"], primary_audit)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    # Diagnostic only: disagreement is recorded and never promotes the claim.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
