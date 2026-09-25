from __future__ import annotations

import subprocess
import sys
from pathlib import Path

CANONICAL_SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "canonical_consensus.py"
)

def main() -> int:
    if not CANONICAL_SCRIPT.exists():
        raise SystemExit(
            "❌ Canonical consensus authority missing: "
            f"{CANONICAL_SCRIPT}"
        )

    completed = subprocess.run(
        [
            sys.executable,
            str(CANONICAL_SCRIPT),
        ],
        check=False,
    )

    return int(
        completed.returncode
    )

if __name__ == "__main__":
    raise SystemExit(
        main()
    )
