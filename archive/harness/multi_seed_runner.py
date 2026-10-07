#!/usr/bin/env python3
import subprocess
import random

SEEDS = 100

results = []

for i in range(SEEDS):
    random.seed(i)
    out = subprocess.check_output(["python", "scripts/adaptive_threshold.py", str(random.random())])
    results.append(out.decode())

print("Runs:", SEEDS)
print("Unique states:", len(set(results)))
