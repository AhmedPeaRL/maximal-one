import os
import json
import numpy as np
import pandas as pd

DATA_DIR = "real-data"
OUT_PATH = "artifacts/null_structure_test.json"

def spectral_alpha(series):

    from scipy.signal import welch

    # 🔥 تنظيف صارم
    x = np.asarray(series, dtype=np.float64)

    # remove NaN / inf
    x = x[np.isfinite(x)]

    if len(x) < 32:
        return np.nan

    # normalization
    x = x - np.mean(x)
    std = np.std(x)

    if std < 1e-10:
        return np.nan

    x = x / std

    freqs, psd = welch(
        x,
        nperseg=min(512, len(x)//4),
        scaling="density"
    )

    mask = freqs > 0
    freqs = freqs[mask]
    psd = psd[mask]

    if len(freqs) < 10:
        return np.nan

    logf = np.log(freqs)
    logp = np.log(psd + 1e-12)

    a, b = np.polyfit(logf, logp, 1)

    if not np.isfinite(a):
        return np.nan

    return float(-a)

def collapse_score(alphas):
    alphas = np.array(alphas)
    return float(np.std(alphas))

def load_series():
    series = []
    for f in os.listdir(DATA_DIR):
        if not f.endswith(".csv"):
            continue
        path = os.path.join(DATA_DIR,f)
        try:
            df = pd.read_csv(path)
            num = df.select_dtypes(include=[np.number])

            if num.shape[1] == 0:
                continue

            s = num.iloc[:, 0].dropna().values
            if len(s) > 256:
                series.append(s)
        except:
            pass
    return series

def shuffle_series(s):
    s = np.array(s)
    np.random.shuffle(s)
    return s

def run_test():

    original = []
    shuffled = []

    series = load_series()

    for s in series:
        original.append(spectral_alpha(s))
        shuffled.append(spectral_alpha(shuffle_series(s)))

    if len(original) == 0:
        raise SystemExit("❌ No valid numeric series found")
    
    orig_score = collapse_score(original)
    shuf_score = collapse_score(shuffled)

    verdict = orig_score < shuf_score

    result = {
        "systems": len(series),
        "original_collapse": orig_score,
        "shuffled_collapse": shuf_score,
        "structure_detected": bool(verdict)
    }

    os.makedirs("artifacts",exist_ok=True)

    with open(OUT_PATH,"w") as f:
        json.dump(result,f,indent=2)

    print(json.dumps(result,indent=2))

if __name__ == "__main__":
    run_test()
