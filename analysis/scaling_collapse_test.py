import numpy as np
import pandas as pd
import glob
import json
from scipy import stats

datasets = glob.glob("real-data/*.csv")

results = []

for path in datasets:
    try:
        df = pd.read_csv(path)

        if df.shape[1] < 2:
            continue

        series = df.iloc[:,1].values.astype(float)

        series = series - np.mean(series)

        spectrum = np.abs(np.fft.rfft(series))**2
        freq = np.fft.rfftfreq(len(series))

        mask = freq > 0
        freq = freq[mask]
        spectrum = spectrum[mask]

        logf = np.log(freq)
        logp = np.log(spectrum)

        slope, intercept, r, p, stderr = stats.linregress(logf,logp)

        results.append({
            "dataset": path,
            "alpha": -slope,
            "r2": r*r
        })

    except Exception:
        continue

alphas = [r["alpha"] for r in results]

output = {
    "datasets": results,
    "mean_alpha": float(np.mean(alphas)) if alphas else None,
    "std_alpha": float(np.std(alphas)) if alphas else None,
    "n_systems": len(alphas)
}

with open("artifacts/scaling_law_test.json","w") as f:
    json.dump(output,f,indent=2)

print(json.dumps(output,indent=2))
