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
    "analysis/witness_lock.py",

    # The reproducibility stamp must be finalized
    # BEFORE the release manifest hashes artifacts.
    "analysis/reproducibility_stamp_guard.py",

    "analysis/freeze_artifacts.py",

    # The release manifest is built only after every
    # artifact included in it has reached its final bytes.
    "analysis/release_manifest_builder.py",
    "analysis/release_manifest_guard.py",

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
