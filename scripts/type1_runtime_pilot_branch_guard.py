from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

AUTHORIZED_REF = "refs/heads/review/type1-v4-remediation"
SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")


def require_authorized_branch() -> None:
    if os.environ.get("GITHUB_ACTIONS") != "true":
        raise SystemExit(
            "BLOCKED: runtime pilot requires GitHub Actions context."
        )

    ref = os.environ.get("GITHUB_REF", "")
    if ref != AUTHORIZED_REF:
        raise SystemExit(
            "BLOCKED: runtime pilot is restricted to "
            f"{AUTHORIZED_REF}; received {ref or 'MISSING GITHUB_REF'}."
        )

    expected_sha = os.environ.get("GITHUB_SHA", "").strip()
    if not SHA_PATTERN.fullmatch(expected_sha):
        raise SystemExit(
            "BLOCKED: runtime pilot requires a full 40-character GITHUB_SHA."
        )

    repository_root = Path(__file__).resolve().parents[1]

    try:
        actual_sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=repository_root,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception as exc:
        raise SystemExit(
            "BLOCKED: cannot verify runtime-pilot checkout identity."
        ) from exc

    if actual_sha != expected_sha:
        raise SystemExit(
            "BLOCKED: runtime-pilot checkout differs from GITHUB_SHA."
        )


def main() -> int:
    require_authorized_branch()
    print(f"Authorized runtime-pilot branch: {AUTHORIZED_REF}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
