from __future__ import annotations

from typing import Any


REQUIRED_PROVENANCE_FIELDS = (
    "source_identifier",
    "source_url_or_citation",
    "physical_domain",
    "observation_variable",
    "sampling_cadence",
    "sampling_regularness",
    "timestamp_presence",
    "time_order",
    "observation_window",
    "missingness_policy",
    "preprocessing_policy",
    "known_shared_nuisance_with_primary",
)

FROZEN_PROTOCOL_STATUSES = {
    "confirmatory_protocol_frozen",
    "frozen_confirmatory_protocol",
}
FROZEN_CONFIRMATORY_STATUSES = {
    "frozen",
    "confirmatory_null_frozen",
}


def protocol_freeze_state(claim: dict[str, Any]) -> tuple[bool, list[str]]:
    """Fail closed unless the protocol is explicitly frozen prospectively."""
    protocol = claim.get("stochastic_null_protocol", {})
    confirmation = protocol.get("confirmatory_status", {})
    reasons: list[str] = []

    if confirmation.get("confirmatory_null_frozen") is not True:
        reasons.append("confirmatory_null_not_frozen")

    if str(confirmation.get("status", "")).strip().lower() not in {
        value.lower() for value in FROZEN_CONFIRMATORY_STATUSES
    }:
        reasons.append("confirmatory_status_not_frozen")

    if str(protocol.get("status", "")).strip().lower() not in {
        value.lower() for value in FROZEN_PROTOCOL_STATUSES
    }:
        reasons.append("protocol_status_not_frozen")

    if protocol.get("preregistered_confirmation") is not True:
        reasons.append("prospective_preregistration_not_confirmed")

    return not reasons, reasons


def provenance_value_present(value: Any) -> bool:
    """Accept explicit False where meaningful, but reject absent metadata."""
    if value is None:
        return False
    if isinstance(value, str):
        normalized = value.strip().lower()
        if not normalized:
            return False
        unresolved_markers = (
            "pending",
            "unverified",
            "not assessed",
            "not reviewed",
            "unknown",
        )
        return not any(marker in normalized for marker in unresolved_markers)
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def candidate_computation_gate(
    candidate: Any,
    expected_path: str,
    protocol_frozen: bool,
) -> tuple[bool, list[str]]:
    """Require a frozen protocol, explicit approval, and complete provenance."""
    reasons: list[str] = []

    if not protocol_frozen:
        reasons.append("confirmatory_protocol_not_frozen")

    if not isinstance(candidate, dict):
        reasons.append("provenance_not_registered")
        return False, reasons

    if candidate.get("path") != expected_path:
        reasons.append("provenance_path_mismatch")

    if candidate.get("replication_eligible") is not True:
        reasons.append("provenance_not_approved_for_replication")

    if candidate.get("explicit_approval") is not True:
        reasons.append("explicit_approval_missing")

    missing = [
        field
        for field in REQUIRED_PROVENANCE_FIELDS
        if not provenance_value_present(candidate.get(field))
    ]
    if missing:
        reasons.append("incomplete_provenance_metadata")
        reasons.extend(f"missing_provenance_field:{field}" for field in missing)

    return not reasons, reasons
