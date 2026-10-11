#!/usr/bin/env python3
"""Diagnostic-only reconciliation of static and run-generated null-capacity state.

This utility records whether the strict claim specification, canonical report,
and null-calibration artifact agree on AR-order boundary diagnostics. It does
not modify scientific inputs, thresholds, null definitions, eligibility, or
claim-promotion authority. A discrepancy is recorded in JSON and exits zero so
that the diagnostic itself does not change existing gate semantics.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

STRICT_CLAIM = Path("core-scientific/strict_claim.json")
CANONICAL_REPORT = Path("artifacts/canonical_report.json")
NULL_GATE = Path("artifacts/null_calibration_gate.json")
OUTPUT = Path("artifacts/null_capacity_state_reconciliation.json")


def nested(data: dict[str, Any], *keys: str) -> Any:
    value: Any = data
    for key in keys:
        if not isinstance(value, dict) or key not in value:
            return None
        value = value[key]
    return value


def close_enough(values: list[Any], tolerance: float = 1e-12) -> bool | None:
    if any(not isinstance(v, (int, float)) or isinstance(v, bool) for v in values):
        return None
    return max(values) - min(values) <= tolerance


def build_report(strict_claim: dict[str, Any], canonical: dict[str, Any], null_gate: dict[str, Any]) -> dict[str, Any]:
    static_review = nested(strict_claim, "stochastic_null_protocol", "model_capacity_review") or {}
    canonical_null = nested(canonical, "appropriate_stochastic_null") or {}
    canonical_diag = canonical_null.get("order_selection_diagnostic") or {}
    gate_diag = null_gate.get("canonical_null_diagnostics") or {}

    values = {
        "strict_claim_surrogate_boundary_fraction": static_review.get("surrogate_boundary_fraction"),
        "canonical_report_surrogate_boundary_fraction": canonical_diag.get("surrogate_boundary_fraction"),
        "null_gate_surrogate_boundary_fraction": gate_diag.get("surrogate_boundary_fraction"),
        "strict_claim_observed_order": static_review.get("observed_selected_order"),
        "canonical_report_selected_order": canonical_null.get("selected_order"),
        "null_gate_selected_order": gate_diag.get("selected_order"),
        "strict_claim_maximum_order": static_review.get("maximum_declared_order"),
        "null_gate_maximum_order": nested(null_gate, "protocol", "max_order"),
    }

    fractions = [
        values["strict_claim_surrogate_boundary_fraction"],
        values["canonical_report_surrogate_boundary_fraction"],
        values["null_gate_surrogate_boundary_fraction"],
    ]
    numeric_fractions = all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in fractions)
    fraction_match = close_enough(fractions) if numeric_fractions else None

    orders = [values["strict_claim_observed_order"], values["canonical_report_selected_order"], values["null_gate_selected_order"]]
    numeric_orders = all(isinstance(v, int) and not isinstance(v, bool) for v in orders)
    order_match = (len(set(orders)) == 1) if numeric_orders else None

    max_orders = [values["strict_claim_maximum_order"], values["null_gate_maximum_order"]]
    numeric_max_orders = all(isinstance(v, int) and not isinstance(v, bool) for v in max_orders)
    maximum_match = (len(set(max_orders)) == 1) if numeric_max_orders else None

    complete = fraction_match is not None and order_match is not None and maximum_match is not None
    all_match = complete and fraction_match and order_match and maximum_match
    return {
        "protocol": "NULL_CAPACITY_STATE_RECONCILIATION_V1",
        "status": "MATCH" if all_match else "RECONCILIATION_REQUIRED",
        "diagnostic_only": True,
        "claim_support": False,
        "promotion_authority": False,
        "scientific_inputs_modified": False,
        "values": values,
        "comparisons": {
            "boundary_fraction_match_within_1e-12": fraction_match,
            "selected_order_match": order_match,
            "maximum_order_match": maximum_match,
        },
        "interpretation": (
            "Static and run-generated null-capacity diagnostics agree."
            if all_match else
            "At least one static/run-generated null-capacity field is missing or differs. Preserve all source values; reconcile exact commit, artifact, and run identity before editing the static specification. This diagnostic does not determine whether the hypothesis is true or false."
        ),
    }


def main() -> int:
    paths = {"strict_claim": STRICT_CLAIM, "canonical_report": CANONICAL_REPORT, "null_gate": NULL_GATE}
    missing = [str(path) for path in paths.values() if not path.is_file()]
    if missing:
        report = {
            "protocol": "NULL_CAPACITY_STATE_RECONCILIATION_V1",
            "status": "INPUTS_MISSING",
            "diagnostic_only": True,
            "claim_support": False,
            "promotion_authority": False,
            "scientific_inputs_modified": False,
            "missing_inputs": missing,
            "interpretation": "Required generated/source JSON is missing; no comparison was made.",
        }
    else:
        loaded = {name: json.loads(path.read_text(encoding="utf-8")) for name, path in paths.items()}
        report = build_report(loaded["strict_claim"], loaded["canonical_report"], loaded["null_gate"])
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    # Intentionally diagnostic-only: disagreement is recorded, not promoted to a new gate.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
