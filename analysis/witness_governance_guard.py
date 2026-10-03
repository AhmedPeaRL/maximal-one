from __future__ import annotations

from pathlib import Path


WORKFLOW_PATH = Path(
    ".github/workflows/scientific-validation.yml"
)

GOVERNANCE_PATH = Path(
    "protocol/WITNESS_GOVERNANCE.md"
)


# These patterns specifically identify witness persistence
# into the Git repository tree.
#
# Generic git commit/push operations are intentionally NOT
# forbidden because the scientific-validation workflow also
# contains legitimate persistence operations unrelated to
# CI witness ingestion.

FORBIDDEN_WITNESS_PERSISTENCE_PATTERNS = (
    "git add data/external/",
    "git add data/external",
    "data/external/witness_",
    "data/external/witness-",
    "git commit -m \"External witness ingestion\"",
    "git commit -m 'External witness ingestion'",
    "External witness ingestion",
)


def fail(message: str) -> None:
    raise SystemExit(
        "❌ WITNESS GOVERNANCE GUARD: "
        + message
    )


def main() -> None:
    if not WORKFLOW_PATH.exists():
        fail(
            f"missing {WORKFLOW_PATH}"
        )

    if not GOVERNANCE_PATH.exists():
        fail(
            f"missing {GOVERNANCE_PATH}"
        )

    workflow = WORKFLOW_PATH.read_text(
        encoding="utf-8"
    )

    for pattern in FORBIDDEN_WITNESS_PERSISTENCE_PATTERNS:
        if pattern in workflow:
            fail(
                "scientific-validation.yml still "
                "contains a forbidden witness-repository "
                f"persistence pattern: {pattern}"
            )

    required_statements = (
        "CI witness != external scientific evidence",
        "CI witness != independent replication",
        "CI witness != canonical scientific result",
        "CI witness != scientific claim support",
    )

    governance = GOVERNANCE_PATH.read_text(
        encoding="utf-8"
    )

    for statement in required_statements:
        if statement not in governance:
            fail(
                "governance document is missing "
                f"required epistemic separation: {statement}"
            )

    print(
        "✅ Witness governance integrity verified."
    )


if __name__ == "__main__":
    main()
