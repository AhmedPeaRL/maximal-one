import json
import glob
import numpy as np

THRESHOLD_STABILITY = 0.85
THRESHOLD_SIGNAL = 2.0

signals = []

for f in glob.glob("artifacts/*.json"):
    try:
        with open(f) as fh:
            data = json.load(fh)
    except:
        continue

    for k,v in data.items():
        if isinstance(v,(int,float)):
            signals.append(v)

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
    "passed": bool(
        snr > THRESHOLD_SIGNAL and
        stability > THRESHOLD_STABILITY
    )
}

print(json.dumps(result,indent=2))
