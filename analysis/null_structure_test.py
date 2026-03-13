import os
import json
import numpy as np
import pandas as pd

DATA_DIR = "real-data"
OUT_PATH = "artifacts/null_structure_test.json"

def spectral_alpha(series):
    x = np.array(series)
    x = x - np.mean(x)
    f = np.fft.rfft(x)
    psd = np.abs(f)**2
    freqs = np.fft.rfftfreq(len(x))
    mask = freqs > 0
    freqs = freqs[mask]
    psd = psd[mask]

    logf = np.log(freqs)
    logp = np.log(psd)

    a,b = np.polyfit(logf,logp,1)
    return -a

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
            col = df.columns[-1]
            s = df[col].dropna().values
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
