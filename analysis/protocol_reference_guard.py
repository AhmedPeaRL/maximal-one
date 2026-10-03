from __future__ import annotations

import json
from pathlib import Path


STRICT_CLAIM_PATH = Path(
    "core-scientific/strict_claim.json"
)

WORKFLOW_PATH = Path(
    ".github/workflows/scientific-validation.yml"
)

UNIFIED_CLAIM_PATH = Path(
    "core-scientific/unified_claim.json"
)


def fail(message: str) -> None:
    raise SystemExit(
        f"❌ PROTOCOL REFERENCE GUARD: {message}"
    )


def main() -> None:
    if not STRICT_CLAIM_PATH.exists():
        fail(f"missing {STRICT_CLAIM_PATH}")

    if not WORKFLOW_PATH.exists():
        fail(f"missing {WORKFLOW_PATH}")

    claim = json.loads(
        STRICT_CLAIM_PATH.read_text(
            encoding="utf-8"
        )
    )

    workflow = WORKFLOW_PATH.read_text(
        encoding="utf-8"
    )

    expected_result = claim.get(
        "expected_result",
        {}
    )

    if "preferred_band" in expected_result:
        fail(
            "strict_claim.json must not contain "
            "the deprecated preferred_band field"
        )

    if "preferred_band_guard.py" in workflow:
        fail(
            "workflow still references the removed "
            "preferred_band_guard.py"
        )

    if "Preferred Band Guard" in workflow:
        fail(
            "workflow still contains the obsolete "
            "Preferred Band Guard step"
        )

    if UNIFIED_CLAIM_PATH.exists():
        unified = json.loads(
            UNIFIED_CLAIM_PATH.read_text(
                encoding="utf-8"
            )
        )

        diagnostic_alpha = unified.get(
            "diagnostic_alpha",
            {}
        )

        if (
            "preferred_band" in diagnostic_alpha
            and diagnostic_alpha.get("role")
            != "diagnostic_only"
        ):
            fail(
                "unified_claim.json contains "
                "preferred_band without diagnostic_only role"
            )

    print(
        "✅ Protocol reference integrity verified"
    )

    print(
        "   strict claim contains no deprecated "
        "preferred-band requirement"
    )

    print(
        "   workflow contains no obsolete "
        "preferred-band guard"
    )

    print(
        "   diagnostic preferred-band metadata, "
        "if present, remains diagnostic-only"
    )


if __name__ == "__main__":
    main()
