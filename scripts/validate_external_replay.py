from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path

REPORT_PATH = Path(
    "artifacts/canonical_report.json"
)

REPLAY_PATH = Path(
    "artifacts/external_replay_verification.json"
)

def finite(value):
    return (
        isinstance(value, (int, float))
        and math.isfinite(float(value))
    )

def fail(message):
    raise SystemExit(
        "EXTERNAL REPLAY GATE FAILURE: "
        + message
    )

def require(condition, message):
    if not condition:
        fail(message)

def sha256_file(path):
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b"",
        ):
            h.update(chunk)

    return h.hexdigest()

def main():
    require(
        REPORT_PATH.exists(),
        "canonical_report.json is missing",
    )

    require(
        REPLAY_PATH.exists(),
        "external_replay_verification.json is missing",
    )

    with REPORT_PATH.open(
        "r",
        encoding="utf-8",
    ) as f:
        report = json.load(f)

    with REPLAY_PATH.open(
        "r",
        encoding="utf-8",
    ) as f:
        replay = json.load(f)

    # ---------------------------------------------------------
    # Canonical report sanity
    # ---------------------------------------------------------

    require(
        isinstance(report, dict),
        "canonical_report.json must contain an object",
    )

    spectral_profile = report.get(
        "spectral_profile"
    )

    require(
        isinstance(spectral_profile, dict),
        "canonical report has no valid spectral_profile",
    )

    canonical_alpha = spectral_profile.get(
        "estimated_alpha"
    )

    require(
        finite(canonical_alpha),
        "canonical alpha is missing or non-finite",
    )

    # ---------------------------------------------------------
    # Independent clean-checkout reproduction artifact schema
    # ---------------------------------------------------------

    required = {
        "independent_replay_verified",
        "fingerprint_match",
        "structure_match",
        "local_fingerprint",
        "external_fingerprint",
        "comparison_method",
        "normalization_precision",
        "volatile_keys_removed",
        "scientific_role",
        "canonical_input_preparation",
        "status",
    }

    missing = (
        required
        -
        set(replay.keys())
    )

    require(
        not missing,
        "missing required fields: "
        + ", ".join(sorted(missing)),
    )

    # ---------------------------------------------------------
    # Boolean gate fields
    # ---------------------------------------------------------

    require(
        replay["independent_replay_verified"] is True,
        "independent_replay_verified is not true",
    )

    require(
        replay["fingerprint_match"] is True,
        "fingerprint_match is not true",
    )

    require(
        replay["structure_match"] is True,
        "structure_match is not true",
    )

    require(
        replay["status"] == "verified",
        "reproduction artifact status is not verified",
    )
    
    # ---------------------------------------------------------
    # Fingerprint validation
    # ---------------------------------------------------------

    local_fingerprint = replay[
        "local_fingerprint"
    ]

    external_fingerprint = replay[
        "external_fingerprint"
    ]

    require(
        isinstance(local_fingerprint, str)
        and len(local_fingerprint) == 64
        and all(
            c in "0123456789abcdef"
            for c in local_fingerprint
        ),
        "local_fingerprint is invalid",
    )

    require(
        isinstance(external_fingerprint, str)
        and len(external_fingerprint) == 64
        and all(
            c in "0123456789abcdef"
            for c in external_fingerprint
        ),
        "external_fingerprint is invalid",
    )

    require(
        local_fingerprint == external_fingerprint,
        "local and independently reproduced fingerprints differ",
    )

    # ---------------------------------------------------------
    # Structural metadata validation
    # ---------------------------------------------------------

    require(
        replay["comparison_method"]
        ==
        "normalized_full_canonical_report",
        (
            "comparison_method must explicitly declare "
            "normalized_full_canonical_report"
        ),
    )

    require(
        replay["normalization_precision"] == 8,
        "unexpected normalization precision",
    )

    require(
        isinstance(
            replay["volatile_keys_removed"],
            list,
        ),
        "volatile_keys_removed must be a list",
    )

    require(
        replay["scientific_role"]
        ==
        "clean_checkout_computational_reproducibility_gate",
        (
            "scientific_role must explicitly identify "
            "the clean-checkout computational reproducibility gate"
        ),
    )

    require(
        replay.get("reproduction_scope")
        ==
        "fresh_public_repository_checkout_same_runner",
        (
            "reproduction scope must explicitly identify "
            "fresh public repository checkout on the same runner"
        ),
    )

    require(
        replay.get("independent_code_checkout")
        is True,
        "independent code checkout is not verified",
    )

    require(
        replay.get("independent_execution_environment")
        is False,
        (
            "execution-environment independence must not "
            "be falsely claimed"
        ),
    )

    require(
        replay.get("external_laboratory_replication")
        is False,
        (
            "external laboratory replication must not "
            "be falsely claimed"
        ),
    )

    require(
        replay.get("independent_implementation_replication")
        is False,
        (
            "independent implementation replication must "
            "not be falsely claimed"
        ),
    )

    require(
        replay.get("independent_scientific_replication")
        is False,
        (
            "independent scientific replication must "
            "not be falsely claimed"
        ),
    )

    require(
        replay.get("verification_scope")
        ==
        "computational_reproducibility_only",
        (
            "verification scope must explicitly limit "
            "the result to computational reproducibility"
        ),
    )

    require(
        isinstance(
            replay.get("source_commit"),
            str,
        )
        and len(replay["source_commit"]) == 40,
        "source_commit must be a full Git commit SHA",
    )

    require(
        replay["canonical_input_preparation"]
        ==
        "scripts/prepare_canonical_inputs.py",
        (
            "canonical input preparation does not match "
            "the canonical protocol"
        ),
    )

    # ---------------------------------------------------------
    # Independent reproduction is NOT the same as an
    # external public-artifact retrieval check.
    #
    # This validator therefore validates exactly what the
    # TRUE independent reproduction script actually proves:
    #
    #   fresh repository clone
    #   exact workflow commit when GITHUB_SHA is available
    #   canonical input reconstruction
    #   independent canonical rerun
    #   normalized full-report comparison
    #   fingerprint equality
    #
    # It does NOT invent external environment fields,
    # report SHA fields, or alpha-delta fields that the
    # producer did not generate.
    # ---------------------------------------------------------

    print(
        "CLEAN-CHECKOUT COMPUTATIONAL REPRODUCIBILITY VERIFIED"
    )

    print(
        "Clean-checkout rerun: TRUE"
    )

    print(
        "Structure match: TRUE"
    )

    print(
        "Fingerprint match: TRUE"
    )

    print(
        "Canonical alpha:",
        float(canonical_alpha),
    )

    print(
        "Local fingerprint:",
        local_fingerprint,
    )

    print(
        "Clean-checkout fingerprint:",
        external_fingerprint,
    )

    print(
        "Comparison method:",
        replay["comparison_method"],
    )

    print(
        "Normalization precision:",
        replay["normalization_precision"],
    )

    print(
        "Scientific role:",
        replay["scientific_role"],
    )

    print(
        "Clean-checkout computational reproducibility gate PASSED."
    )

if __name__ == "__main__":
    main()
