#!/usr/bin/env python3
"""Add explanatory eligibility labels without changing any gate decisions.

This module only enriches artifacts/dataset_eligibility_gate.json with
human-readable diagnostic fields. It does not change any existing eligibility
boolean, domain count, status, threshold, or exit code.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ARTIFACT = Path("artifacts/dataset_eligibility_gate.json")
PROTOCOL = "ELIGIBILITY_DIAGNOSTIC_LABELS_V1"


def _append_unique(target: list[str], value: Any) -> None:
    if isinstance(value, str) and value and value != "eligible" and value not in target:
        target.append(value)


def enrich_domain(item: dict[str, Any]) -> dict[str, Any]:
    """Return a copy with explanatory labels; preserve all existing fields."""
    out = dict(item)
    measurement = item.get("eligible_for_measurement", item.get("measurement_valid", False)) is True
    replication = item.get("eligible_for_replication", item.get("replication_eligible", False)) is True
    provenance = item.get("provenance_replication_eligible", False) is True
    primary = item.get("primary_domain") is True
    derived = item.get("derived_domain") is True

    if measurement:
        structural_status = "MEASUREMENT_VALID"
    elif item.get("status") == "ERROR":
        structural_status = "EVALUATION_ERROR"
    else:
        structural_status = "MEASUREMENT_INVALID"

    reasons: list[str] = []
    if primary:
        final_status = "EXCLUDED_PRIMARY_DOMAIN"
        _append_unique(reasons, "primary_domain_excluded_from_secondary_replication_count")
    elif derived:
        final_status = "EXCLUDED_DERIVED_DOMAIN"
        _append_unique(reasons, "derived_or_related_domain_excluded")
    elif not measurement:
        final_status = "INELIGIBLE_STRUCTURALLY"
        _append_unique(reasons, item.get("reason"))
        _append_unique(reasons, item.get("replication_exclusion_reason"))
    elif not replication:
        final_status = "NOT_REPLICATION_ELIGIBLE"
        _append_unique(reasons, item.get("reason"))
        _append_unique(reasons, item.get("replication_exclusion_reason"))
        _append_unique(reasons, item.get("provenance_exclusion_reason"))
        review = item.get("provenance_review")
        if isinstance(review, dict):
            _append_unique(reasons, review.get("reason"))
    elif not provenance:
        final_status = "NOT_REPLICATION_ELIGIBLE"
        _append_unique(reasons, item.get("provenance_exclusion_reason"))
        review = item.get("provenance_review")
        if isinstance(review, dict):
            _append_unique(reasons, review.get("reason"))
    else:
        final_status = "REPLICATION_ELIGIBLE_CANDIDATE"

    out["diagnostic_labels"] = {
        "protocol": PROTOCOL,
        "structural_status": structural_status,
        "final_replication_status": final_status,
        "final_replication_reasons": reasons,
        "explanatory_only": True,
        "does_not_change_gate_decisions": True,
    }
    return out


def enrich_report(report: dict[str, Any]) -> dict[str, Any]:
    out = dict(report)
    domains = report.get("domains")
    if isinstance(domains, list):
        out["domains"] = [enrich_domain(item) if isinstance(item, dict) else item for item in domains]
    out["diagnostic_label_protocol"] = PROTOCOL
    out["diagnostic_labels_only"] = True
    out["existing_gate_decisions_modified"] = False
    return out


def main() -> int:
    if not ARTIFACT.is_file():
        raise SystemExit(f"ERROR: required eligibility artifact is missing: {ARTIFACT}")
    report = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    enriched = enrich_report(report)
    ARTIFACT.write_text(json.dumps(enriched, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("ELIGIBILITY DIAGNOSTIC LABELS ADDED (explanatory fields only)")
    print(f"Existing gate status preserved: {enriched.get('status')}")
    print(f"Existing eligible replication count preserved: {enriched.get('eligible_replication_domain_count')}")
    for item in enriched.get("domains", []):
        labels = item.get("diagnostic_labels", {})
        print(f"- {item.get('name', 'UNKNOWN')}: structural={labels.get('structural_status')}; final={labels.get('final_replication_status')}; reasons={labels.get('final_replication_reasons', [])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
