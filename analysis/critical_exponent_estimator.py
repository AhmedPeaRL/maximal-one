import numpy as np
import pandas as pd
from pathlib import Path
import json

DATA_DIR = "real-data"
OUT = "artifacts/critical_exponents.json"


def spectral_alpha(x):

    x = np.asarray(x)
    x = x - np.mean(x)

    f = np.fft.rfft(x)
    psd = np.abs(f)**2

    freqs = np.fft.rfftfreq(len(x))

    mask = (freqs > 0)

    freqs = freqs[mask]
    psd = psd[mask]

    logf = np.log(freqs)
    logp = np.log(psd)

    slope = np.polyfit(logf, logp,1)[0]

    return -slope


def hurst(x):

    x = np.asarray(x)

    N = len(x)

    T = np.arange(1,N+1)

    Y = np.cumsum(x-np.mean(x))

    R = np.maximum.accumulate(Y)-np.minimum.accumulate(Y)

    S = np.std(x)

    if S==0:
        return np.nan

    return np.log(R[-1]/S)/np.log(N)


def estimate(series):

    return {
        "alpha": spectral_alpha(series),
        "hurst": hurst(series)
    }


def run():

    results = {}

    for f in Path(DATA_DIR).glob("*.csv"):

        try:

            df = pd.read_csv(f)

            col = df.columns[0]

            x = df[col].dropna().values

            if len(x)<200:
                continue

            results[f.name] = estimate(x)

        except Exception:
            pass

    Path("artifacts").mkdir(exist_ok=True)

    with open(OUT,"w") as f:
        json.dump(results,f,indent=2)

    print(json.dumps(results,indent=2))


if __name__=="__main__":
    run()
