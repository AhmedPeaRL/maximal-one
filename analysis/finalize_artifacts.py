from __future__ import annotations
import os
import subprocess

PRE_EXTERNAL_STAGES = [
    "analysis/environment_fingerprint.py",
    "analysis/dataset_provenance_guard.py",
    "analysis/pipeline_sovereignty_guard.py",
    "analysis/estimator_calibration_guard.py",
    "analysis/provenance_chain_guard.py",
    "analysis/normalize_artifacts.py",
    "analysis/replay_lock.py",
    "analysis/full_replay_consistency_guard.py",
    "analysis/report_hash_manifest.py",
    "analysis/external_replay_verifier.py",
]

FINAL_STAGES = PRE_EXTERNAL_STAGES + [
    # The final canonical report is already sealed by the workflow
    # before FINALIZE_PHASE=final begins.

    # Rebuild the reproducibility manifest AFTER the final
    # canonical_report.json bytes are fixed.
    "analysis/build_reproducibility_manifest.py",

    # The reproducibility stamp must also be generated from the
    # same final canonical report bytes before release sealing.
    "analysis/reproducibility_stamp_guard.py",

    # Bind the authoritative witness only after all upstream
    # scientific/reproducibility artifacts are final.
    "analysis/witness_lock.py",

    # Freeze the final scientific artifact set.
    "analysis/freeze_artifacts.py",

    # Build the release manifest only after every artifact that
    # belongs to that manifest has reached final bytes.
    "analysis/release_manifest_builder.py",

    # Verify that no artifact included in the release manifest
    # changed after sealing.
    "analysis/release_manifest_guard.py",

    # These artifacts are generated after release-manifest sealing
    # and therefore are intentionally outside that manifest.
    "analysis/temporal_sovereignty_guard.py",

    "analysis/final_state_lock.py",
]

phase = os.getenv(
    "FINALIZE_PHASE",
    "pre_external"
).strip().lower()

if phase == "pre_external":
    stages = PRE_EXTERNAL_STAGES

elif phase == "final":
    stages = FINAL_STAGES

else:
    raise SystemExit(
        "❌ Unknown FINALIZE_PHASE. "
        "Use 'pre_external' or 'final'."
    )

for script in stages:
    print(
        f"\n=== RUNNING {script} ({phase}) ===\n"
    )

    subprocess.run(
        ["python", script],
        check=True
    )

print(
    f"\n✅ ARTIFACT FINALIZATION COMPLETE: {phase}"
)
