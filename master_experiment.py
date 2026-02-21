#!/usr/bin/env python3
import subprocess

MODES = ["noise", "shift", "adversarial"]

for mode in MODES:
    print("MODE:", mode)

    data = subprocess.check_output(
        ["python", "harness/real_data_loader.py", "data/input.csv"]
    ).decode().splitlines()

    for d in data:
        p = subprocess.check_output(
            ["python", "harness/perturbation.py", d, mode]
        ).decode().strip()

        subprocess.run(
            ["python", "scripts/adaptive_threshold.py", p]
        )

    subprocess.run(["python", "harness/lyapunov_monitor.py"])
    subprocess.run(["python", "harness/equilibrium_test.py"])
