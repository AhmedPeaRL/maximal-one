import subprocess

ARTIFACT_STAGES = [

    # foundational sealing
    "analysis/environment_fingerprint.py",
    "analysis/dataset_provenance_guard.py",
    "analysis/pipeline_sovereignty_guard.py",
    "analysis/estimator_calibration_guard.py",
    "analysis/provenance_chain_guard.py",
    "analysis/full_replay_consistency_guard.py",
    "analysis/external_replay_verifier.py",
    "analysis/witness_lock.py",

    # normalize EVERYTHING first
    "analysis/normalize_artifacts.py",

    # temporal verification BEFORE closure sealing
    "analysis/temporal_sovereignty_guard.py",

    # freeze immutable closure AFTER temporal validation
    "analysis/freeze_artifacts.py",

    # final immutable state
    "analysis/final_state_lock.py"
]

for script in ARTIFACT_STAGES:

    print(f"\n=== RUNNING {script} ===\n")

    subprocess.run(
        ["python", script],
        check=True
    )

print("\n✅ ALL ARTIFACTS FINALIZED")
