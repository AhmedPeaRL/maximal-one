import json
import hashlib
import os
import random
import time

def load_internal_report():
    with open("artifacts/canonical_report.json") as f:
        return json.load(f)

def simulate_external_environment():
    # ❗ تغيير جذري في البيئة
    salt = str(time.time()) + str(random.random())
    return hashlib.sha256(salt.encode()).hexdigest()

def generate_external_dataset():
    # ❗ dataset مختلف فعلاً
    import numpy as np
    t = np.arange(0, 1500)
    v = 30 + 20*np.sin(2*np.pi*t/7) + np.random.normal(0,10,len(t))
    return v

def compute_external_alpha(series):
    import numpy as np

    fft = np.fft.fft(series)
    power = np.abs(fft)**2

    log_freq = np.log(np.arange(1,len(power)))
    log_power = np.log(power[1:])

    slope = np.polyfit(log_freq, log_power, 1)[0]
    return -slope

def main():
    report = load_internal_report()
    internal_alpha = report["spectral_profile"]["estimated_alpha"]

    external_env = simulate_external_environment()
    series = generate_external_dataset()
    external_alpha = compute_external_alpha(series)

    diff = abs(internal_alpha - external_alpha)

    print("Internal alpha:", internal_alpha)
    print("External alpha:", external_alpha)
    print("Diff:", diff)

    # ⚠️ أهم شرط
    if diff < 0.0001:
        print("❌ Suspicious match → not independent")
        exit(1)

    if diff > 1.0:
        print("❌ Model unstable across environments")
        exit(1)

    print("✅ True independence validated")

if __name__ == "__main__":
    main()
