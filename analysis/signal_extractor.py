import json
import glob
import numpy as np
import math

THRESHOLD_STABILITY = 0.85
THRESHOLD_SIGNAL = 2.0

signals = []

def extract_numbers(obj):
    if isinstance(obj, dict):
        for v in obj.values():
            extract_numbers(v)

    elif isinstance(obj, list):
        for v in obj:
            extract_numbers(v)

    elif isinstance(obj,(int,float)):
        if not math.isnan(v:=float(obj)) and not math.isinf(v):
            signals.append(v)


for f in glob.glob("artifacts/*.json"):
    try:
        with open(f) as fh:
            data = json.load(fh)
        extract_numbers(data)

    except Exception:
        continue


if not signals:
    print(json.dumps({"status":"no-data"}))
    exit(0)

signals = np.array(signals)

mean = float(np.mean(signals))
std = float(np.std(signals))

snr = abs(mean)/(std+1e-9)
stability = 1/(1+std)

result = {
    "mean_signal":mean,
    "std":std,
    "snr":snr,
    "stability":stability,
    "samples":len(signals),
    "passed": bool(
        snr > THRESHOLD_SIGNAL and
        stability > THRESHOLD_STABILITY
    )
}

print(json.dumps(result,indent=2))
