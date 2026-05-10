import subprocess
from pathlib import Path

ARTIFACTS = [
    "analysis/environment_fingerprint.py",
    "analysis/dataset_provenance_guard.py",
    "analysis/pipeline_sovereignty_guard.py",
    "analysis/estimator_calibration_guard.py",
    "analysis/provenance_chain_guard.py",
    "analysis/full_replay_consistency_guard.py",
    "analysis/witness_lock.py",
    "analysis/artifact_closure_guard.py",
    "analysis/temporal_sovereignty_guard.py"
]

for script in ARTIFACTS:

    print(f"\n=== RUNNING {script} ===\n")

    subprocess.run(
        ["python", script],
        check=True
    )

print("\n✅ ALL ARTIFACTS FINALIZED")
