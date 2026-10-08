from __future__ import annotations

import json
from pathlib import Path

from analysis.load_real_datasets import DATASETS


REGISTRY_PATH = Path(
    "protocol/REPLICATION_PROVENANCE_REGISTRY_V1.json"
)

PRIMARY_NAMES = {
    "sunspots",
}

DERIVED_NAMES = {
    "extended",
}


def main() -> int:
    if not REGISTRY_PATH.is_file():
        raise SystemExit(
            f"Missing provenance registry: {REGISTRY_PATH}"
        )

    registry = json.loads(
        REGISTRY_PATH.read_text(encoding="utf-8")
    )

    if registry.get("protocol") != (
        "REPLICATION_PROVENANCE_REGISTRY_V1"
    ):
        raise SystemExit(
            "Unexpected provenance registry protocol."
        )

    candidates = registry.get("candidates")

    if not isinstance(candidates, dict):
        raise SystemExit(
            "Registry candidates must be a JSON object."
        )

    errors = []

    for name, path in DATASETS.items():
        if name in PRIMARY_NAMES or name in DERIVED_NAMES:
            continue

        candidate = candidates.get(name)

        if not isinstance(candidate, dict):
            errors.append(
                f"{name}: missing provenance registry entry"
            )
            continue

        if candidate.get("path") != path:
            errors.append(
                f"{name}: registry path mismatch "
                f"(expected {path!r}, got "
                f"{candidate.get('path')!r})"
            )

    if errors:
        print("REPLICATION INVENTORY: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("REPLICATION INVENTORY: PASS")
    print(
        "All secondary datasets in the loader "
        "have matching registry names and paths."
    )
    print(
        "This check does not establish provenance "
        "completeness or scientific replication."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
