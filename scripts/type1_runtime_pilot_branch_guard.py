from __future__ import annotations

import os
import sys

AUTHORIZED_REF = "refs/heads/review/type1-v4-remediation"


def require_authorized_branch(actual_ref: str | None = None) -> None:
    ref = (
        actual_ref
        if actual_ref is not None
        else os.environ.get("GITHUB_REF", "")
    )

    if ref != AUTHORIZED_REF:
        raise SystemExit(
            "BLOCKED: runtime pilot is restricted to "
            f"{AUTHORIZED_REF}; received {ref or 'MISSING GITHUB_REF'}."
        )


def main() -> int:
    require_authorized_branch()
    print(f"Authorized runtime-pilot branch: {AUTHORIZED_REF}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
