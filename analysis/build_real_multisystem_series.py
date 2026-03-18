import json
import numpy as np
import pandas as pd
import pathlib

ART = pathlib.Path("artifacts")
DATA = pathlib.Path("real-data")

def load_csv_series(path):
    df = pd.read_csv(path)

    numeric = df.select_dtypes(include=['number'])
    if numeric.shape[1] == 0:
        return None

    s = numeric.iloc[:, 0].dropna().values

    if len(s) < 500:
        return None

    s = (s - np.mean(s)) / (np.std(s) + 1e-8)

    return s

systems = {
    "sunspots": "real-data/sunspots_global_prepared.csv",
    "climate": "real-data/climate.csv",
    "internet": "real-data/internet_traffic.csv",
    "eeg": "real-data/eeg.csv"
}

ART.mkdir(exist_ok=True)

for name, path in systems.items():

    if not pathlib.Path(path).exists():
        print(f"{name} missing — skipped")
        continue

    series = load_csv_series(path)

    if series is None:
        print(f"{name} invalid — skipped")
        continue

    model = np.random.permutation(series)

    (ART / f"{name}_real.json").write_text(json.dumps(series.tolist()))
    (ART / f"{name}_model.json").write_text(json.dumps(model.tolist()))

    print(f"{name} processed:", len(series))
