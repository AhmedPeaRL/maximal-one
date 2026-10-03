from __future__ import annotations

from pathlib import Path


WORKFLOW_PATH = Path(
    ".github/workflows/scientific-validation.yml"
)

GOVERNANCE_PATH = Path(
    "protocol/WITNESS_GOVERNANCE.md"
)


FORBIDDEN_WORKFLOW_PATTERNS = (
    "git add data/external/",
    "External witness ingestion",
    "git push",
    "git commit",
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

    for pattern in FORBIDDEN_WORKFLOW_PATTERNS:
        if pattern in workflow:
            fail(
                "scientific-validation.yml still "
                f"contains forbidden witness-persistence "
                f"pattern: {pattern}"
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
