import numpy as np
import pandas as pd
import glob
import json
from scipy.interpolate import interp1d

datasets = glob.glob("real-data/*.csv")

collapsed_curves = []

for path in datasets:
    try:
        df = pd.read_csv(path)

        if df.shape[1] < 2:
            continue

        series = df.iloc[:,1].values.astype(float)

        series = series - np.mean(series)
        series = series / np.std(series)

        spec = np.abs(np.fft.rfft(series))**2
        freq = np.fft.rfftfreq(len(series))

        mask = freq > 0
        freq = freq[mask]
        spec = spec[mask]

        # rescale
        freq = freq / np.max(freq)
        spec = spec / np.max(spec)

        collapsed_curves.append((freq,spec,path))

    except Exception:
        continue

grid = np.linspace(0.001,1,500)

interp_curves = []

for f,s,name in collapsed_curves:
    try:
        interp = interp1d(f,s,bounds_error=False,fill_value=np.nan)
        interp_curves.append(interp(grid))
    except:
        pass

arr = np.array(interp_curves)

mean_curve = np.nanmean(arr,axis=0)
std_curve = np.nanstd(arr,axis=0)

collapse_score = float(np.nanmean(std_curve))

result = {
    "systems": len(interp_curves),
    "collapse_score": collapse_score,
    "interpretation": "lower means stronger universal scaling"
}

with open("artifacts/scaling_collapse_engine.json","w") as f:
    json.dump(result,f,indent=2)

print(json.dumps(result,indent=2))
