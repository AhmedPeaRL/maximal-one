import subprocess
import sys

scripts = [
    "stability/linear_family_certification.py",
    "stability/nonlinear_lasalle_gate.py",
    "stability/symbolic_proof_generator.py",
    "integrity/cryptographic_stamp.py"
]

for script in scripts:
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise RuntimeError(f"Pipeline failed at {script}")

print("Full reproducible research pipeline passed.")
