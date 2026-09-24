from __future__ import annotations
import hashlib
import json
from pathlib import Path

CANONICAL_REPORT = Path(
    "artifacts/canonical_report.json"
)

REPLAY_ARTIFACT = Path(
    "artifacts/external_replay_verification.json"
)

OUTPUT = Path(
    "artifacts/reproducibility_manifest.json"
)

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b"",
        ):
            h.update(chunk)

    return h.hexdigest()

def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(
            "REPRODUCIBILITY MANIFEST FAILURE: "
            + message
        )

def main() -> None:
    require(
        CANONICAL_REPORT.exists(),
        "canonical_report.json is missing",
    )

    require(
        REPLAY_ARTIFACT.exists(),
        "external_replay_verification.json is missing",
    )

    with CANONICAL_REPORT.open(
        "r",
        encoding="utf-8",
    ) as f:
        report = json.load(f)

    with REPLAY_ARTIFACT.open(
        "r",
        encoding="utf-8",
    ) as f:
        replay = json.load(f)

    require(
        isinstance(report, dict),
        "canonical report must be a JSON object",
    )

    require(
        isinstance(replay, dict),
        "replay artifact must be a JSON object",
    )

    canonical_alpha = (
        report
        .get("spectral_profile", {})
        .get("estimated_alpha")
    )

    require(
        isinstance(canonical_alpha, (int, float)),
        "canonical alpha is missing",
    )

    independent_rerun = (
        replay.get(
            "independent_replay_verified"
        )
        is True
    )

    fingerprint_match = (
        replay.get(
            "fingerprint_match"
        )
        is True
    )

    structure_match = (
        replay.get(
            "structure_match"
        )
        is True
    )

    final_replay_verified = bool(
        independent_rerun
        and fingerprint_match
        and structure_match
    )

    manifest = {
        "schema_version": "1.0",

        "canonical_report_sha256":
            sha256_file(
                CANONICAL_REPORT
            ),

        "canonical_alpha":
            float(canonical_alpha),

        "canonical_claim_status":
            report
            .get("scientific_interpretation", {})
            .get(
                "claim_status",
                "unknown",
            ),

        "canonical_claim_support_gate":
            bool(
                report
                .get(
                    "scientific_interpretation",
                    {},
                )
                .get(
                    "claim_support_gate",
                    False,
                )
            ),

        "canonical_claim_support_gate_snapshot":
            bool(
                report
                .get(
                    "scientific_interpretation",
                    {},
                )
                .get(
                    "claim_support_gate",
                    False,
                )
            ),

        "reproducibility_gate":
            {
                "independent_rerun_verified":
                    independent_rerun,

                "fingerprint_match":
                    fingerprint_match,

                "structure_match":
                    structure_match,

                "verified":
                    final_replay_verified,
            },

        "independent_rerun_verified":
            independent_rerun,

        "fingerprint_match":
            fingerprint_match,

        "structure_match":
            structure_match,

        "replay_status":
            replay.get(
                "status",
                "unknown",
            ),

        "local_fingerprint":
            replay.get(
                "local_fingerprint"
            ),

        "external_fingerprint":
            replay.get(
                "external_fingerprint"
            ),

        "comparison_method":
            replay.get(
                "comparison_method"
            ),

        "normalization_precision":
            replay.get(
                "normalization_precision"
            ),

        "scientific_role":
            replay.get(
                "scientific_role"
            ),

        "verification_scope":
            replay.get(
                "verification_scope"
            ),

        "reproducibility_status":
            (
                "verified"
                if final_replay_verified
                else "not_verified"
            ),

        "reproducibility_scope": {
            "code_checkout":
                "fresh_public_checkout",

            "repository_state":
                "exact_workflow_commit",

            "execution_environment":
                "same_runner",

            "input_reconstruction":
                "canonical_deterministic_rebuild",

            "implementation_independence":
                False,

            "laboratory_independence":
                False,

            "external_scientific_replication":
                False,

            "scope":
                "computational_reproducibility_only",
        },

        "interpretation":
            (
                "The canonical scientific report is "
                "preserved as an immutable experiment "
                "snapshot. Reproducibility verification "
                "is represented separately by the "
                "independent replay artifact and this "
                "manifest. A verified rerun does not by "
                "itself establish mechanism, universality, "
                "consciousness, NEF, HCM causation, or "
                "resolution of the Hard Problem."
            ),
    }

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT.open(
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            manifest,
            f,
            indent=2,
        )
        f.write("\n")

    print(
        "REPRODUCIBILITY MANIFEST"
    )

    print(
        "Canonical report SHA256:",
        manifest[
            "canonical_report_sha256"
        ],
    )

    print(
        "Independent rerun:",
        independent_rerun,
    )

    print(
        "Fingerprint match:",
        fingerprint_match,
    )

    print(
        "Structure match:",
        structure_match,
    )

    print(
        "Reproducibility status:",
        manifest[
            "reproducibility_status"
        ],
    )

    if not final_replay_verified:
        raise SystemExit(
            "❌ Reproducibility verification is not complete"
        )

    print(
        "✅ Reproducibility manifest verified"
    )

if __name__ == "__main__":
    main()
