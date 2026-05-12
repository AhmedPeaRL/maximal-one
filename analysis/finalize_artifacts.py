import subprocess

ARTIFACT_STAGES = [

    "analysis/environment_fingerprint.py",
    "analysis/dataset_provenance_guard.py",
    "analysis/pipeline_sovereignty_guard.py",
    "analysis/estimator_calibration_guard.py",
    "analysis/provenance_chain_guard.py",

    # normalize FIRST
    "analysis/normalize_artifacts.py",

    # deterministic replay
    "analysis/replay_lock.py",
    "analysis/full_replay_consistency_guard.py",

    # manifest + provenance
    "analysis/report_hash_manifest.py",
    "analysis/external_replay_verifier.py",
    "analysis/witness_lock.py",

    # immutable freeze
    "analysis/freeze_artifacts.py",

    # release closure
    "analysis/release_manifest_builder.py",
    "analysis/release_manifest_guard.py",
    "analysis/reproducibility_stamp_guard.py",

    # FINAL TEMPORAL SNAPSHOT
    "analysis/temporal_sovereignty_guard.py",

    # absolute final lock
    "analysis/final_state_lock.py"
]

for script in ARTIFACT_STAGES:

    print(f"\n=== RUNNING {script} ===\n")

    subprocess.run(
        ["python", script],
        check=True
    )

print("\n✅ ALL ARTIFACTS FINALIZED")
