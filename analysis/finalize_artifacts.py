import subprocess

ARTIFACT_STAGES = [

    "analysis/environment_fingerprint.py",
    "analysis/dataset_provenance_guard.py",
    "analysis/pipeline_sovereignty_guard.py",
    "analysis/estimator_calibration_guard.py",
    "analysis/provenance_chain_guard.py",

    # normalize FIRST
    "analysis/normalize_artifacts.py",
    "analysis/replay_lock.py",

    # THEN verify replay
    "analysis/full_replay_consistency_guard.py",

    "analysis/report_hash_manifest.py",
    "analysis/external_replay_verifier.py",
    "analysis/witness_lock.py",

    # immutable freeze
    "analysis/freeze_artifacts.py",

    # build immutable manifest AFTER freeze
    "analysis/release_manifest_builder.py",

    # verify manifest
    "analysis/release_manifest_guard.py",

    # temporal check AFTER freeze
    "analysis/temporal_sovereignty_guard.py",

    # final lock
    "analysis/final_state_lock.py"
]

for script in ARTIFACT_STAGES:

    print(f"\n=== RUNNING {script} ===\n")

    subprocess.run(
        ["python", script],
        check=True
    )

print("\n✅ ALL ARTIFACTS FINALIZED")
