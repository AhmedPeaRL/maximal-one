from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

AUTHORIZED_REF = "refs/heads/review/type1-v4-remediation"
SHA40 = re.compile(r"^[0-9a-fA-F]{40}$")
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def require_authorized_branch(actual_ref: str | None = None) -> None:
    ref = actual_ref if actual_ref is not None else os.environ.get("GITHUB_REF", "")
    if ref != AUTHORIZED_REF:
        raise SystemExit(
            "BLOCKED: runtime pilot is restricted to "
            f"{AUTHORIZED_REF}; received {ref or 'MISSING GITHUB_REF'}."
        )

    if os.environ.get("GITHUB_ACTIONS", "").lower() != "true":
        raise SystemExit(
            "BLOCKED: runtime pilot requires the GitHub Actions execution context."
        )

    expected_sha = os.environ.get("GITHUB_SHA", "")
    if not SHA40.fullmatch(expected_sha):
        raise SystemExit(
            "BLOCKED: runtime pilot requires a non-empty full 40-character GITHUB_SHA."
        )

    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise SystemExit(
            "BLOCKED: runtime pilot could not verify the checked-out Git commit."
        ) from exc

    actual_head = result.stdout.strip()
    if actual_head.lower() != expected_sha.lower():
        raise SystemExit(
            "BLOCKED: runtime pilot checkout does not match GITHUB_SHA "
            f"(HEAD={actual_head or 'UNKNOWN'})."
        )


def main() -> int:
    require_authorized_branch()
    print(f"Authorized runtime-pilot branch and checkout: {AUTHORIZED_REF}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
