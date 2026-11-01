from __future__ import annotations

import re
from typing import Any

CONTEXT_RADIUS = 5

RUNNER_RE = re.compile(
    r"""
    (?:python(?:3)?\s+)
    (?:
        -m\s+
        (?:analysis\.)?
        (?:calibrate_null_type1(?:_scenario)?|type1_calibration_pilot)
        |
        (?:analysis/)?calibrate_null_type1(?:_scenario)?\.py
        |
        (?:analysis/)?type1_calibration_pilot\.py
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)

GOVERNANCE_RE = re.compile(
    r"confirmatory_execution_authorized|"
    r"formal_calibration_pass|"
    r"promotion_authority|"
    r"claim_support|"
    r"freeze_state|"
    r"APPROVED_FROZEN|"
    r"V4_APPROVED",
    re.IGNORECASE,
)

GUARD_RE = re.compile(
    r"fail.closed|not authorized|not approved|"
    r"exit\s+1|freeze_state|APPROVED_FROZEN|"
    r"confirmatory_execution_authorized",
    re.IGNORECASE,
)

PROPOSAL_RE = re.compile(
    r"\b(candidate|proposed|proposal|draft|pending approval|"
    r"not approved|decision request)\b",
    re.IGNORECASE,
)

HISTORICAL_RE = re.compile(
    r"\b(historical|superseded|previously|prior run|"
    r"legacy result|historical result)\b",
    re.IGNORECASE,
)

DIAGNOSTIC_RE = re.compile(
    r"\b(diagnostic|audit.only|engineering.only|"
    r"exploratory|operating.characteristics|test.only)\b",
    re.IGNORECASE,
)


def _normalize_context(
    context_window: list[dict[str, Any]] | None,
    occurrence_line: int,
) -> list[dict[str, Any]]:
    if context_window is None:
        return []
    if not isinstance(context_window, list):
        raise ValueError("context_window must be a list")

    normalized = []
    for item in context_window:
        if not isinstance(item, dict):
            raise ValueError("context entries must be objects")
        line_number = item.get("line")
        line_text = item.get("text")
        if (
            isinstance(line_number, bool)
            or not isinstance(line_number, int)
            or line_number < 1
        ):
            raise ValueError("context line numbers must be positive integers")
        if not isinstance(line_text, str):
            raise ValueError("context text must be a string")
        if abs(line_number - occurrence_line) > CONTEXT_RADIUS:
            continue
        normalized.append({"line": line_number, "text": line_text})
    return sorted(normalized, key=lambda item: item["line"])


def classify_occurrence(
    *,
    path: str,
    line: int,
    matched_text: str,
    context_window: list[dict[str, Any]] | None,
) -> dict[str, Any]:
    """Return a conservative occurrence-local discovery suggestion only.

    This function never creates a manual classification, closes a ledger
    record, verifies a complete call graph, or grants execution authority.
    A nearby runner invocation is not sufficient to classify this occurrence
    as an execution path; the matched occurrence itself must be the invocation.
    """
    if not isinstance(path, str) or not path:
        raise ValueError("path must be a non-empty string")
    if isinstance(line, bool) or not isinstance(line, int) or line < 1:
        raise ValueError("line must be a positive integer")
    if not isinstance(matched_text, str):
        raise ValueError("matched_text must be a string")

    local = _normalize_context(context_window, line)
    if not any(item["line"] == line for item in local):
        local.append({"line": line, "text": matched_text})
        local.sort(key=lambda item: item["line"])

    local_text = "\n".join(item["text"] for item in local)
    occurrence_text = matched_text
    occurrence_is_runner = bool(RUNNER_RE.search(occurrence_text))
    nearby_runner_lines = [
        item["line"] for item in local
        if item["line"] != line and RUNNER_RE.search(item["text"])
    ]
    guard_lines = [
        item["line"] for item in local if GUARD_RE.search(item["text"])
    ]
    governance_match = bool(GOVERNANCE_RE.search(occurrence_text))

    if occurrence_is_runner:
        suggestion = "EXECUTION_PATH_CANDIDATE_UNVERIFIED"
        rationale = (
            "The matched occurrence itself is a runner invocation. Full "
            "direct/indirect call-path and authorization-order review remains required."
        )
        evidence = {
            "runner_occurrence_line": line,
            "nearby_runner_reference_lines": nearby_runner_lines,
            "nearby_guard_candidate_lines": guard_lines,
            "guard_order_verified": False,
        }
    elif governance_match:
        suggestion = "GOVERNANCE"
        rationale = (
            "The matched occurrence itself names an authorization, promotion, "
            "freeze, or claim-state control."
        )
        evidence = {
            "matched_occurrence_is_governance_field": True,
            "nearby_guard_candidate_lines": guard_lines,
            "nearby_runner_reference_lines": nearby_runner_lines,
        }
    elif PROPOSAL_RE.search(local_text):
        suggestion = "PROPOSAL"
        rationale = "Proposal or candidate language occurs within the bounded occurrence-local context."
        evidence = {"nearby_runner_reference_lines": nearby_runner_lines}
    elif HISTORICAL_RE.search(local_text):
        suggestion = "HISTORICAL"
        rationale = "Historical or superseded language occurs within the bounded occurrence-local context."
        evidence = {"nearby_runner_reference_lines": nearby_runner_lines}
    elif DIAGNOSTIC_RE.search(local_text):
        suggestion = "DIAGNOSTIC"
        rationale = "Diagnostic, audit, exploratory, or engineering-only language occurs within the bounded occurrence-local context."
        evidence = {"nearby_runner_reference_lines": nearby_runner_lines}
    else:
        suggestion = "UNKNOWN"
        rationale = (
            "The bounded occurrence-local evidence is insufficient for "
            "a defensible automated suggestion."
        )
        evidence = {"nearby_runner_reference_lines": nearby_runner_lines}

    return {
        "classifier": "TYPE1_OCCURRENCE_LOCAL_CLASSIFIER_P1",
        "context_radius_lines": CONTEXT_RADIUS,
        "suggested_classification": suggestion,
        "rationale": rationale,
        "evidence": evidence,
        "manual_review_required": True,
        "manual_classification": "UNKNOWN",
        "status": "OPEN",
        "reviewer_disposition": "PENDING",
        "execution_authority": False,
        "classification_is_human_adjudication": False,
    }
