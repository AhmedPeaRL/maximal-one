import json
import glob
import numpy as np
import math

THRESHOLD_SNR = 0.5
THRESHOLD_STABILITY = 0.2

signals = []

TARGET_KEYS = [
    "lyapunov_exp",
    "alpha",
    "estimated_alpha",
    "collapse_score",
    "collapse_error",
    "hurst",
    "correlation_dimension"
]

def extract(obj):

    if isinstance(obj, dict):
        for k,v in obj.items():

            if k in TARGET_KEYS and isinstance(v,(int,float)):
                if not math.isnan(v) and not math.isinf(v):
                    signals.append(float(v))

            extract(v)

    elif isinstance(obj,list):
        for v in obj:
            extract(v)


for f in glob.glob("artifacts/*.json"):
    try:
        with open(f) as fh:
            data=json.load(fh)
        extract(data)
    except:
        pass


if not signals:
    print(json.dumps({"status":"no-invariants"}))
    exit(0)


signals=np.array(signals)

# 🧠 بدل ما نصفر البيانات — نحافظ على معناها
mean=float(np.mean(signals))
std=float(np.std(signals))

snr=abs(mean)/(std+1e-9)

# stability: هل القيم متقاربة؟
stability=float(1/(1+std))

# dispersion structure (ده مهم جدًا)
skew=float(np.mean((signals-mean)**3)/(std**3 + 1e-9))

result={
    "samples":len(signals),
    "mean_signal":mean,
    "std":std,
    "snr":snr,
    "stability":stability,
    "skewness":skew,
    "passed":bool(
        snr>THRESHOLD_SNR and
        stability>THRESHOLD_STABILITY
    )
}

print(json.dumps(result,indent=2))
