import json
import math
from pathlib import Path


REGISTRY_PATH = Path(
    "protocol/NULL_ADEQUACY_THRESHOLD_REGISTRY_V1.json"
)

REQUIRED_DIMENSIONS = (
    "residual_autocorrelation",
    "residual_partial_autocorrelation",
    "stationarity",
    "parameter_stability",
    "finite_sample_calibration",
    "surrogate_validity",
    "model_selection_stability",
    "boundary_saturation",
    "effective_sample_size_preservation",
    "nuisance_structure_preservation",
)


def fail(message):
    raise SystemExit(f"❌ {message}")


def main():
    if not REGISTRY_PATH.exists():
        fail(
            f"Missing threshold registry: {REGISTRY_PATH}"
        )

    with REGISTRY_PATH.open(
        encoding="utf-8"
    ) as f:
        registry = json.load(f)

    if registry.get("protocol") != (
        "NULL_ADEQUACY_THRESHOLD_REGISTRY_V1"
    ):
        fail("Unexpected threshold registry protocol.")

    status = registry.get("status")

    dimensions = registry.get(
        "required_dimensions",
        {}
    )

    missing_dimensions = [
        name
        for name in REQUIRED_DIMENSIONS
        if name not in dimensions
    ]

    if missing_dimensions:
        fail(
            "Missing required adequacy dimensions: "
            + ", ".join(missing_dimensions)
        )

    for name in REQUIRED_DIMENSIONS:
        if dimensions[name].get("required") is not True:
            fail(
                f"Required adequacy dimension is not marked "
                f"required: {name}"
            )

    if status == "NOT_FROZEN":
        print(
            "ℹ️ Null adequacy thresholds are NOT_FROZEN."
        )
        print(
            "ℹ️ Confirmatory null selection remains blocked."
        )
        return 0

    if status != "FROZEN":
        fail(
            f"Unsupported threshold registry status: {status}"
        )

    prerequisites = registry.get(
        "confirmation_prerequisites",
        {}
    )

    required_prerequisites = (
        "calibration_dataset_frozen",
        "candidate_family_frozen",
        "adequacy_thresholds_frozen",
        "nuisance_treatment_frozen",
        "surrogate_generator_frozen",
        "replication_registry_frozen",
    )

    for key in required_prerequisites:
        if prerequisites.get(key) is not True:
            fail(
                f"Frozen registry is missing required "
                f"confirmation prerequisite: {key}"
            )

    for name in REQUIRED_DIMENSIONS:
        item = dimensions[name]

        if item.get("threshold_frozen") is not True:
            fail(
                f"Threshold is not frozen for dimension: {name}"
            )

        threshold = item.get("threshold")

        if threshold is None:
            fail(
                f"Frozen threshold is null for dimension: {name}"
            )

        if isinstance(threshold, bool):
            fail(
                f"Frozen threshold must be numeric: {name}"
            )

        if not isinstance(threshold, (int, float)):
            fail(
                f"Frozen threshold is not numeric: {name}"
            )

        if not math.isfinite(float(threshold)):
            fail(
                f"Frozen threshold is not finite: {name}"
            )

    if registry.get("preregistered_confirmation") is not True:
        fail(
            "Frozen confirmatory thresholds require "
            "preregistered_confirmation=true."
        )

    print(
        "✅ Null adequacy threshold registry is "
        "structurally frozen and complete."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
