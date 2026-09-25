from __future__ import annotations

import subprocess
import sys
from pathlib import Path

CANONICAL_SCRIPT = Path(
    "scripts/canonical_consensus.py"
)

def main() -> None:
    if not CANONICAL_SCRIPT.exists():
        raise SystemExit(
            "Canonical consensus authority is missing: "
            f"{CANONICAL_SCRIPT}"
        )

    print(
        "Canonical consensus guard delegates exclusively "
        "to scripts/canonical_consensus.py"
    )

    subprocess.run(
        [
            sys.executable,
            str(CANONICAL_SCRIPT),
        ],
        check=True,
    )

    print(
        "Canonical consensus guard completed without "
        "maintaining a competing scientific definition."
    )

if __name__ == "__main__":
    main()
