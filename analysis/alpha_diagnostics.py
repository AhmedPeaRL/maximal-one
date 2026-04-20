import json
import numpy as np

with open("artifacts/canonical_report.json") as f:
    r = json.load(f)

alpha = r["spectral_profile"]["estimated_alpha"]
sigma = r["spectral_profile"]["bootstrap_std"]

print("=== ALPHA DIAGNOSTICS ===")
print("alpha:", alpha)
print("sigma:", sigma)

if alpha > 3:
    print("⚠️ Likely scaling error (FFT/log mismatch)")

if sigma > 1:
    print("⚠️ Bootstrap instability / insufficient sample")

if alpha > 5 and sigma > 1:
    print("🚨 SYSTEMIC FAILURE: signal is dominated by noise or misfit")

ratio = alpha / (sigma + 1e-9)
print("alpha/sigma ratio:", ratio)

if ratio < 1:
    print("⚠️ weak signal vs noise")

print("=== END ===")
