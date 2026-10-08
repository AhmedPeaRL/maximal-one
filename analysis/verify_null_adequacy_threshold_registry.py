import hashlib
import json
import math
import subprocess
from pathlib import Path


REGISTRY_PATH = Path(
    "protocol/NULL_ADEQUACY_THRESHOLD_REGISTRY_V1.json"
)

FREEZE_LOCK_PATH = Path(
    "protocol/NULL_ADEQUACY_FREEZE_LOCK_V1.json"
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


def sha256_file(path):
    digest = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def git_output(*args):
    try:
        return subprocess.check_output(
            ["git", *args],
            text=True,
            stderr=subprocess.STDOUT,
        ).strip()
    except Exception as exc:
        fail(
            "Git metadata is unavailable: "
            + str(exc)
        )


def verify_freeze_lock(registry):
    if not FREEZE_LOCK_PATH.exists():
        fail(
            "FROZEN registry requires "
            "NULL_ADEQUACY_FREEZE_LOCK_V1.json."
        )

    with FREEZE_LOCK_PATH.open(
        encoding="utf-8"
    ) as f:
        lock = json.load(f)

    if lock.get("protocol") != (
        "NULL_ADEQUACY_FREEZE_LOCK_V1"
    ):
        fail(
            "Unexpected null adequacy freeze lock protocol."
        )

    freeze_commit = lock.get(
        "freeze_commit"
    )

    registry_sha256 = lock.get(
        "registry_sha256"
    )

    if not isinstance(
        freeze_commit,
        str,
    ) or len(freeze_commit) != 40:
        fail(
            "freeze_commit must be a full 40-character SHA."
        )

    if not isinstance(
        registry_sha256,
        str,
    ) or len(registry_sha256) != 64:
        fail(
            "registry_sha256 must be a SHA-256 digest."
        )

    actual_hash = sha256_file(
        REGISTRY_PATH
    )

    if actual_hash != registry_sha256:
        fail(
            "Frozen registry SHA-256 does not match "
            "the current registry contents."
        )

    head = git_output(
        "rev-parse",
        "HEAD",
    )

    if freeze_commit == head:
        fail(
            "Freeze commit must precede the "
            "confirmation run commit."
        )

    try:
        subprocess.check_call(
            [
                "git",
                "merge-base",
                "--is-ancestor",
                freeze_commit,
                head,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        fail(
            "Freeze commit is not an ancestor of "
            "the current confirmation run."
        )
    
    try:
        frozen_registry_bytes = subprocess.check_output(
            [
                "git",
                "show",
                f"{freeze_commit}:{REGISTRY_PATH.as_posix()}",
            ],
            text=False,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as exc:
        detail = (
            exc.stderr.decode("utf-8", errors="replace").strip()
            if exc.stderr
            else "Git could not retrieve the registry at that commit."
        )
        fail(
            "Cannot verify the frozen registry at "
            f"commit {freeze_commit}. Check that the commit exists "
            "and contains "
            f"{REGISTRY_PATH.as_posix()}. Details: {detail}"
        )

    frozen_commit_hash = hashlib.sha256(
        frozen_registry_bytes
    ).hexdigest()

    if frozen_commit_hash != registry_sha256:
        fail(
            "The registry contents at freeze_commit do not "
            "match the registry_sha256 recorded in the freeze lock."
        )

    if frozen_commit_hash != actual_hash:
        fail(
            "The registry changed after the declared freeze commit."
        )

    print(
        "✅ Null adequacy freeze provenance verified."
    )
    print(
        "   freeze commit:",
        freeze_commit,
    )
    print(
        "   confirmation commit:",
        head,
    )
    print(
        "   registry SHA-256:",
        actual_hash,
    )


def main():
    if not REGISTRY_PATH.exists():
        fail(
            f"Missing threshold registry: "
            f"{REGISTRY_PATH}"
        )

    with REGISTRY_PATH.open(
        encoding="utf-8"
    ) as f:
        registry = json.load(f)

    if registry.get("protocol") != (
        "NULL_ADEQUACY_THRESHOLD_REGISTRY_V1"
    ):
        fail(
            "Unexpected threshold registry protocol."
        )

    dimensions = registry.get(
        "required_dimensions",
        {},
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
        if dimensions[name].get(
            "required"
        ) is not True:
            fail(
                f"Required adequacy dimension is not "
                f"marked required: {name}"
            )

    status = registry.get(
        "status"
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
            f"Unsupported threshold registry status: "
            f"{status}"
        )

    prerequisites = registry.get(
        "confirmation_prerequisites",
        {},
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
                "Frozen registry is missing required "
                f"confirmation prerequisite: {key}"
            )

    if registry.get(
        "preregistered_confirmation"
    ) is not True:
        fail(
            "Frozen confirmatory thresholds require "
            "preregistered_confirmation=true."
        )

    for name in REQUIRED_DIMENSIONS:
        item = dimensions[name]

        if item.get(
            "threshold_frozen"
        ) is not True:
            fail(
                f"Threshold is not frozen for dimension: "
                f"{name}"
            )

        threshold = item.get(
            "threshold"
        )

        if threshold is None:
            fail(
                f"Frozen threshold is null for dimension: "
                f"{name}"
            )

        if isinstance(
            threshold,
            bool,
        ):
            fail(
                f"Frozen threshold must be numeric: "
                f"{name}"
            )

        if not isinstance(
            threshold,
            (int, float),
        ):
            fail(
                f"Frozen threshold is not numeric: "
                f"{name}"
            )

        if not math.isfinite(
            float(threshold)
        ):
            fail(
                f"Frozen threshold is not finite: "
                f"{name}"
            )

        bounds = item.get("allowed_bounds")

        if not isinstance(bounds, dict):
            fail(
                f"Frozen threshold requires allowed_bounds: {name}"
            )

        lower = bounds.get("minimum")
        upper = bounds.get("maximum")

        for label, value in (
            ("minimum", lower),
            ("maximum", upper),
        ):
            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not math.isfinite(float(value))
            ):
                fail(
                    f"Invalid allowed_bounds.{label}: {name}"
                )

        if float(lower) > float(upper):
            fail(f"Reversed allowed_bounds: {name}")

        if not float(lower) <= float(threshold) <= float(upper):
            fail(
                f"Threshold falls outside declared bounds: {name}"
            )

        for field in (
            "metric_definition",
            "units",
            "calibration_rationale",
            "calibration_reference",
        ):
            value = item.get(field)
            if not isinstance(value, str) or not value.strip():
                fail(
                    f"Frozen threshold requires {field}: {name}"
        )

    verify_freeze_lock(
        registry
    )

    print(
        "✅ Null adequacy threshold registry is "
        "structurally frozen, complete, and "
        "provenance-locked."
    )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
