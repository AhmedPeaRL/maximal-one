import json
import glob
import numpy as np
import math

# ---- thresholds ----
THRESHOLD_SIGNAL = 0.8
THRESHOLD_STABILITY = 0.2

signals = []

# invariants we care about
TARGET_KEYS = [
    "lyapunov_exp",
    "alpha",
    "estimated_alpha",
    "collapse_score",
    "collapse_error",
    "hurst",
    "correlation_dimension"
]

def extract_invariants(obj):

    if isinstance(obj, dict):
        for k,v in obj.items():

            if k in TARGET_KEYS and isinstance(v,(int,float)):
                if not math.isnan(v) and not math.isinf(v):
                    signals.append(float(v))

            extract_invariants(v)

    elif isinstance(obj,list):
        for v in obj:
            extract_invariants(v)


for f in glob.glob("artifacts/*.json"):

    try:
        with open(f) as fh:
            data=json.load(fh)

        extract_invariants(data)

    except:
        pass


if not signals:
    print(json.dumps({
        "status":"no-invariants"
    }))
    exit(0)


signals=np.array(signals)

# normalize
signals=(signals-np.mean(signals))/(np.std(signals)+1e-9)

mean=float(np.mean(signals))
std=float(np.std(signals))

snr=abs(mean)/(std+1e-9)

stability=float(1/(1+std))

result={
    "samples":len(signals),
    "mean_signal":mean,
    "std":std,
    "snr":snr,
    "stability":stability,
    "passed":bool(
        snr>THRESHOLD_SIGNAL and
        stability>THRESHOLD_STABILITY
    )
}

print(json.dumps(result,indent=2))
