from __future__ import annotations

import json
from pathlib import Path

from analysis.load_real_datasets import DATASETS


REGISTRY_PATH = Path(
    "protocol/REPLICATION_PROVENANCE_REGISTRY_V1.json"
)

PRIMARY_NAMES = {"sunspots"}
DERIVED_NAMES = {"extended"}


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

    errors: list[str] = []
    informational: list[str] = []

    # Direction 1:
    # Every loaded secondary dataset must have a matching registry entry.
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
                f"(loader={path!r}, registry="
                f"{candidate.get('path')!r})"
            )

    # Direction 2:
    # Every registry candidate must be accounted for in the loader.
    # Pending, explicitly ineligible candidates may remain un-loaded,
    # but they must not claim replication eligibility.
    for name, candidate in candidates.items():
        if not isinstance(candidate, dict):
            errors.append(
                f"{name}: registry candidate must be an object"
            )
            continue

        registry_path = candidate.get("path")
        eligible = candidate.get("replication_eligible")

        if not isinstance(registry_path, str) or not registry_path:
            errors.append(
                f"{name}: missing or invalid registry path"
            )
            continue

        if eligible not in (True, False):
            errors.append(
                f"{name}: replication_eligible must be "
                "explicitly true or false"
            )
            continue

        loader_path = DATASETS.get(name)

        if loader_path is None:
            if eligible is True:
                errors.append(
                    f"{name}: marked replication-eligible "
                    "but absent from the dataset loader"
                )
            else:
                informational.append(
                    f"{name}: registered but not loaded; "
                    "remains ineligible for replication"
                )
            continue

        if loader_path != registry_path:
            errors.append(
                f"{name}: loader/registry path mismatch "
                f"(loader={loader_path!r}, "
                f"registry={registry_path!r})"
            )

    if errors:
        print("REPLICATION INVENTORY: FAIL")
        for error in errors:
            print(f"- {error}")

        for item in informational:
            print(f"INFO: {item}")

        return 1

    print("REPLICATION INVENTORY: PASS")
    print(
        "Loader-to-registry and registry-to-loader "
        "consistency checks passed."
    )

    for item in informational:
        print(f"INFO: {item}")

    print(
        "Inventory consistency does not establish provenance "
        "completeness, independent replication, or claim promotion."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
