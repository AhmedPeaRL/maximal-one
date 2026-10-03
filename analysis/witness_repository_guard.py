from __future__ import annotations

import json
from pathlib import Path


WITNESS_DIR = Path(
    "data/external"
)

MAX_TRACKED_WITNESSES = 10


def main() -> None:
    if not WITNESS_DIR.exists():
        print(
            "✅ Witness repository guard: "
            "data/external does not exist."
        )
        return

    witnesses = sorted(
        WITNESS_DIR.glob(
            "witness_*.json"
        )
    )

    count = len(witnesses)

    print(
        f"Tracked witness files: {count}"
    )

    if count > MAX_TRACKED_WITNESSES:
        raise SystemExit(
            "❌ Witness repository guard failed: "
            f"{count} tracked witnesses exceed "
            f"the maximum of {MAX_TRACKED_WITNESSES}. "
            "CI witnesses must remain run artifacts, "
            "not accumulated Git history."
        )

    for path in witnesses:
        try:
            payload = json.loads(
                path.read_text(
                    encoding="utf-8"
                )
            )
        except Exception as exc:
            raise SystemExit(
                "❌ Witness repository guard failed: "
                f"invalid JSON in {path}: {exc}"
            )

        if payload.get("_empty") is True:
            raise SystemExit(
                "❌ Witness repository guard failed: "
                f"empty CI witness remains tracked: {path}"
            )

    print(
        "✅ Witness repository guard passed."
    )


if __name__ == "__main__":
    main()
