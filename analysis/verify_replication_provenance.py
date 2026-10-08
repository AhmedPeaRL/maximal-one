from __future__ import annotations

import json
from pathlib import Path


REGISTRY = Path(
    "protocol/REPLICATION_PROVENANCE_REGISTRY_V1.json"
)

PROVENANCE_DIR = Path(
    "protocol/provenance"
)

REQUIRED_FIELDS = (
    "source_identifier",
    "source_url_or_citation",
    "physical_domain",
    "observation_variable",
    "sampling_cadence",
    "sampling_regularness",
    "timestamp_presence",
    "time_order",
    "observation_window",
    "missingness_policy",
    "preprocessing_policy",
    "known_shared_nuisance_with_primary",
)


def fail(message: str) -> None:
    raise SystemExit(
        f"PROVENANCE GATE BLOCKED: {message}"
    )


def nonempty(value) -> bool:
    if value is None:
        return False

    if isinstance(value, str):
        return bool(value.strip())

    return True


def main() -> None:
    if not REGISTRY.is_file():
        fail(f"missing registry: {REGISTRY}")

    registry = json.loads(
        REGISTRY.read_text(
            encoding="utf-8"
        )
    )

    candidates = registry.get(
        "candidates",
        {}
    )

    if not isinstance(candidates, dict):
        fail("registry candidates must be an object")

    failures = []
    eligible_count = 0

    for name, candidate in candidates.items():

        if not isinstance(candidate, dict):
            failures.append(
                f"{name}: invalid registry entry"
            )
            continue

        if candidate.get(
            "replication_eligible"
        ) is not True:
            continue

        eligible_count += 1

        provenance_file = (
            PROVENANCE_DIR
            / f"{name}_v1.json"
        )

        if not provenance_file.is_file():
            failures.append(
                f"{name}: approved dataset has no provenance file"
            )
            continue

        record = json.loads(
            provenance_file.read_text(
                encoding="utf-8"
            )
        )

        source = record.get(
            "source",
            {}
        )

        observation = record.get(
            "observation",
            {}
        )

        data_handling = record.get(
            "data_handling",
            {}
        )

        independence = record.get(
            "independence",
            {}
        )

        values = {
            "source_identifier":
                source.get("source_identifier"),

            "source_url_or_citation":
                source.get("source_url_or_citation"),

            "physical_domain":
                observation.get("physical_domain"),

            "observation_variable":
                observation.get("observation_variable"),

            "sampling_cadence":
                observation.get("sampling_cadence"),

            "sampling_regularness":
                observation.get("sampling_regularness"),

            "timestamp_presence":
                observation.get("timestamp_presence"),

            "time_order":
                observation.get("time_order"),

            "observation_window":
                observation.get("observation_window"),

            "missingness_policy":
                data_handling.get("missingness_policy"),

            "preprocessing_policy":
                data_handling.get("preprocessing_policy"),

            "known_shared_nuisance_with_primary":
                independence.get(
                    "known_shared_nuisance_with_primary"
                ),
        }

        missing = [
            key
            for key, value in values.items()
            if not nonempty(value)
        ]

        if missing:
            failures.append(
                f"{name}: missing required provenance fields: "
                + ", ".join(missing)
            )

        review = record.get(
            "review",
            {}
        )

        if (
            review.get(
                "approved_for_replication"
            )
            is not True
        ):
            failures.append(
                f"{name}: replication approval is not explicit"
            )

    if failures:
        for failure in failures:
            print(f"- {failure}")

        raise SystemExit(
            1
        )

    if eligible_count == 0:
        print(
            "PROVENANCE GATE: NO APPROVED CANDIDATES VERIFIED"
        )
        print(
            "No provenance approval was established; "
            "replication remains blocked."
        )
        return

    print("PROVENANCE GATE: PASS")
    print(
        f"Approved candidate provenance records verified: "
        f"{eligible_count}"
    )


if __name__ == "__main__":
    main()
